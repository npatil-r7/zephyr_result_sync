"""
Zephyr Scale Robot Framework Listener

Enterprise-level listener for automatic test result synchronization
with Zephyr Scale Cloud v2 API.

Usage:
    robot --listener ZephyrListener tests/

Environment Variables Required:
    ZEPHYR_API_KEY    - Zephyr Scale API Bearer Token
    ZEPHYR_PROJECT_KEY - Jira Project Key (e.g., R7QE)
    
Optional Environment Variables:
    ZEPHYR_BASE_URL   - API Base URL (default: EU region)
    ZEPHYR_FOLDER_ID  - Folder ID for test cases
"""

import os
import re
import requests
from datetime import datetime
from typing import Dict, Optional, List

try:
    import pytz
except ImportError:
    pytz = None


class ZephyrListener:
    """
    Robot Framework Listener for Zephyr Scale Cloud Integration
    
    Implements ROBOT_LISTENER_API_VERSION 3 for automatic test result
    synchronization with Zephyr Scale Cloud v2 API.
    """
    
    # =========================================================================
    # LISTENER CONFIGURATION
    # =========================================================================
    
    ROBOT_LISTENER_API_VERSION = 3
    
    # Zephyr Scale Cloud API Base URLs
    # EU Region: https://eu.api.zephyrscale.smartbear.com/v2
    # US Region: https://api.zephyrscale.smartbear.com/v2
    DEFAULT_BASE_URL = "https://eu.api.zephyrscale.smartbear.com/v2"
    
    # Indian Standard Time timezone
    IST_TIMEZONE = "Asia/Kolkata"
    
    # =========================================================================
    # INITIALIZATION
    # =========================================================================
    
    def __init__(self):
        """Initialize the Zephyr Listener with environment configuration."""
        
        print("\n" + "=" * 70)
        print("🚀 [ZEPHYR] Initializing Zephyr Scale Listener...")
        print("=" * 70)
        
        # Load configuration from environment variables
        self.api_key = os.environ.get("ZEPHYR_API_KEY")
        self.project_key = os.environ.get("ZEPHYR_PROJECT_KEY")
        self.base_url = os.environ.get("ZEPHYR_BASE_URL", self.DEFAULT_BASE_URL)
        self.folder_id = os.environ.get("ZEPHYR_FOLDER_ID")
        
        # Runtime state
        self.test_cycle_key = None
        self.is_enabled = True
        self.results_synced = 0
        self.results_skipped = 0
        self.results_failed = 0
        
        # Validate required configuration
        self._validate_configuration()
        
        # Setup HTTP headers
        if self.is_enabled:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            print(f"✅ [ZEPHYR] Configuration loaded successfully")
            print(f"   📍 Base URL: {self.base_url}")
            print(f"   📁 Project Key: {self.project_key}")
            if self.folder_id:
                print(f"   📂 Folder ID: {self.folder_id}")
        
        print("=" * 70 + "\n")
    
    def _validate_configuration(self):
        """Validate required environment variables."""
        
        errors = []
        
        if not self.api_key:
            errors.append("ZEPHYR_API_KEY")
        
        if not self.project_key:
            errors.append("ZEPHYR_PROJECT_KEY")
        
        if errors:
            print("\n" + "!" * 70)
            print("❌ [ZEPHYR] CRITICAL: Missing required environment variables!")
            print("!" * 70)
            for var in errors:
                print(f"   ⚠️  {var} is not set")
            print("\n   To fix, run:")
            print(f"   export ZEPHYR_API_KEY='your_api_key_here'")
            print(f"   export ZEPHYR_PROJECT_KEY='your_project_key_here'")
            print("\n   Zephyr sync will be DISABLED for this run.")
            print("!" * 70 + "\n")
            self.is_enabled = False
    
    # =========================================================================
    # TIMEZONE UTILITIES
    # =========================================================================
    
    def _get_ist_timestamp(self) -> str:
        """
        Get current timestamp in Indian Standard Time (IST).
        
        Returns:
            Formatted timestamp string: Automation Test Cycle 24th Mar 2026 2:30 PM
        """
        if pytz:
            ist = pytz.timezone(self.IST_TIMEZONE)
            now = datetime.now(ist)
        else:
            # Fallback to UTC if pytz not available
            now = datetime.utcnow()
            print("⚠️ [ZEPHYR] pytz not installed, using UTC time")
        
        # Get day with ordinal suffix (1st, 2nd, 3rd, 4th, etc.)
        day = now.day
        if 11 <= day <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        
        # Format: TestCycle 24th Feb 2026 8:10 PM
        formatted_date = now.strftime(f"%-d{suffix} %b %Y %-I:%M %p")
        return f"Automation Test Cycle {formatted_date}"
    
    def _get_iso_timestamp(self) -> str:
        """
        Get current timestamp in ISO 8601 format for API calls.
        
        Returns:
            ISO formatted timestamp string
        """
        if pytz:
            ist = pytz.timezone(self.IST_TIMEZONE)
            now = datetime.now(ist)
        else:
            now = datetime.utcnow()
        
        return now.strftime("%Y-%m-%dT%H:%M:%S%z")
    
    # =========================================================================
    # HTTP REQUEST HANDLER
    # =========================================================================
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make HTTP request to Zephyr API with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT)
            endpoint: API endpoint
            data: Request payload
        
        Returns:
            Response JSON or None on failure
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 401:
                print(f"❌ [ZEPHYR] Error 401: Unauthorized - API key is invalid or expired")
                return None
            
            if response.status_code == 404:
                print(f"❌ [ZEPHYR] Error 404: Resource not found - {endpoint}")
                return None
            
            if not response.ok:
                print(f"❌ [ZEPHYR] Error {response.status_code}: {response.text[:200]}")
                return None
            
            return response.json() if response.text else {}
        
        except requests.exceptions.Timeout:
            print(f"❌ [ZEPHYR] Request timeout for {endpoint}")
            return None
        
        except requests.exceptions.ConnectionError:
            print(f"❌ [ZEPHYR] Connection error - Unable to reach Zephyr API")
            return None
        
        except Exception as e:
            print(f"❌ [ZEPHYR] Unexpected error: {str(e)}")
            return None
    
    # =========================================================================
    # TAG EXTRACTION
    # =========================================================================
    
    def _extract_test_case_key(self, tags: List[str]) -> Optional[str]:
        """
        Extract Zephyr test case key from Robot Framework tags.
        
        Args:
            tags: List of test tags
        
        Returns:
            Test case key (e.g., 'R7QE-T4080') or None
        """
        # Dynamic pattern based on project_key
        pattern = rf"{self.project_key}-T\d+"
        
        for tag in tags:
            if re.match(pattern, str(tag)):
                return tag
        
        return None
    
    # =========================================================================
    # LISTENER EVENTS
    # =========================================================================
    
    def start_suite(self, data, result):
        """
        Called when a test suite starts.
        Creates a new Test Cycle in Zephyr Scale.
        
        Args:
            data: Suite data object
            result: Suite result object
        """
        if not self.is_enabled:
            return
        
        # Only create test cycle for the top-level suite
        if data.parent is None:
            self._create_test_cycle(data.name)
    
    def end_test(self, data, result):
        """
        Called when a test case ends.
        Syncs test result to Zephyr Scale.
        
        Args:
            data: Test data object
            result: Test result object
        """
        if not self.is_enabled:
            return
        
        if not self.test_cycle_key:
            print(f"⚠️ [ZEPHYR] Skipping: No test cycle available for test '{data.name}'")
            self.results_skipped += 1
            return
        
        # Extract test case key from tags
        test_case_key = self._extract_test_case_key(data.tags)
        
        if not test_case_key:
            print(f"⚠️ [ZEPHYR] Skipping: No Jira Key found for test '{data.name}'")
            print(f"   Tags found: {list(data.tags)}")
            print(f"   Expected pattern: {self.project_key}-T<number>")
            self.results_skipped += 1
            return
        
        # Map Robot Framework status to Zephyr status
        status = "Pass" if result.passed else "Fail"
        
        # Sync result to Zephyr
        self._sync_test_result(test_case_key, status, data.name, result.message)
    
    def end_suite(self, data, result):
        """
        Called when a test suite ends.
        Prints summary for top-level suite.
        
        Args:
            data: Suite data object
            result: Suite result object
        """
        if not self.is_enabled:
            return
        
        # Only print summary for top-level suite
        if data.parent is None:
            self._print_summary()
    
    # =========================================================================
    # ZEPHYR API OPERATIONS
    # =========================================================================
    
    def _create_test_cycle(self, suite_name: str):
        """
        Create a new Test Cycle in Zephyr Scale.
        
        Args:
            suite_name: Name of the Robot Framework test suite
        """
        cycle_name = self._get_ist_timestamp()
        
        print(f"\n📋 [ZEPHYR] Creating Test Cycle: {cycle_name}")
        
        payload = {
            "projectKey": self.project_key,
            "name": cycle_name,
            "description": f"Automated test run for suite: {suite_name}",
            "statusName": "Not Executed"
        }
        
        # Add folder if configured
        if self.folder_id:
            payload["folderId"] = int(self.folder_id)
        
        try:
            response = self._make_request("POST", "/testcycles", payload)
            
            if response and "key" in response:
                self.test_cycle_key = response["key"]
                print(f"✅ [ZEPHYR] Test Cycle created: {self.test_cycle_key}")
            else:
                print(f"❌ [ZEPHYR] Failed to create Test Cycle")
                print(f"   Response: {response}")
        
        except Exception as e:
            print(f"❌ [ZEPHYR] Error creating Test Cycle: {str(e)}")
            # Don't disable - continue without cycle
    
    def _sync_test_result(self, test_case_key: str, status: str, test_name: str, message: str = None):
        """
        Sync test result to Zephyr Scale.
        
        Args:
            test_case_key: Zephyr test case key
            status: Test status (Pass/Fail)
            test_name: Robot Framework test name
            message: Optional failure message
        """
        print(f"\n🔄 [ZEPHYR] Syncing: {test_case_key} ({test_name})")
        
        payload = {
            "projectKey": self.project_key,
            "testCaseKey": test_case_key,
            "testCycleKey": self.test_cycle_key,
            "statusName": status,
            "executedById": None,  # Will use API token owner
            "assignedToId": None
        }
        
        # Add comment for failed tests
        if status == "Fail" and message:
            # Truncate message if too long
            comment = message[:500] if len(message) > 500 else message
            payload["comment"] = f"Failure reason: {comment}"
        
        try:
            response = self._make_request("POST", "/testexecutions", payload)
            
            if response:
                status_emoji = "✅" if status == "Pass" else "❌"
                print(f"{status_emoji} [ZEPHYR] Synced: {test_case_key} → {status}")
                self.results_synced += 1
            else:
                print(f"❌ [ZEPHYR] Failed to sync: {test_case_key}")
                self.results_failed += 1
        
        except Exception as e:
            print(f"❌ [ZEPHYR] Error syncing {test_case_key}: {str(e)}")
            self.results_failed += 1
            # Don't raise - keep the test green
    
    def _print_summary(self):
        """Print final sync summary."""
        
        total = self.results_synced + self.results_skipped + self.results_failed
        
        print("\n" + "=" * 70)
        print("📊 [ZEPHYR] Sync Summary")
        print("=" * 70)
        
        if self.test_cycle_key:
            print(f"   📋 Test Cycle: {self.test_cycle_key}")
        
        print(f"   ✅ Synced:  {self.results_synced}")
        print(f"   ⚠️  Skipped: {self.results_skipped}")
        print(f"   ❌ Failed:  {self.results_failed}")
        print(f"   📈 Total:   {total}")
        print("=" * 70 + "\n")