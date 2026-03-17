import requests
import re
from typing import Dict, Optional, List

class ZephyrSync:
    """Zephyr Scale Cloud API synchronization for Robot Framework."""
    
    # Your Bearer Token
    BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL3JhcGlkNy5hdGxhc3NpYW4ubmV0IiwidXNlciI6eyJhY2NvdW50SWQiOiI3MTIwMjA6ZTdhYmU5NDItY2RmOS00ZGQyLWE2YzMtYmFhYjg2MmRhMzc5IiwidG9rZW5JZCI6ImNlNTIyODljLTg3MzAtNDQzZC1hNDQwLWNlNTVjN2I1YWUyMSJ9fSwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJzdWIiOiJhYzNkNzMzMS1hZTExLTM1M2MtOTY4Zi0zMjQ4NzNlMDYyNWMiLCJleHAiOjE4MDQ5MTk5NjIsImlhdCI6MTc3MzM4Mzk2Mn0.G98jaTkWBp--qg_NV7rebJMhLpvtNerrcNN5mmp1pcw"
    
    # EU Zephyr Scale Cloud API endpoint
    BASE_URL = "https://eu.api.zephyrscale.smartbear.com/v2"
    
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def __init__(self, bearer_token: str = None):
        self.bearer_token = bearer_token or self.BEARER_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        print("[INFO] Zephyr API initialized (EU)")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Zephyr API"""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            print(f"[DEBUG] {method} request to: {url}")
            
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            print(f"[DEBUG] Response status: {response.status_code}")
            
            if response.status_code == 401:
                print("✗ ERROR: 401 Unauthorized - Token is invalid or expired")
                raise Exception("Invalid or expired Bearer Token")
            
            response.raise_for_status()
            return response.json() if response.text else {}
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code}")
            print(f"Response: {e.response.text}")
            raise
    
    def extract_zephyr_key_from_tags(self, tags: List[str]) -> Optional[str]:
        """
        Search tags list for Zephyr test case key matching pattern R7QE-T\d+
        
        Args:
            tags: List of tags from Robot Framework test
        
        Returns:
            Zephyr test case key if found (e.g., 'R7QE-T4080'), None otherwise
        """
        pattern = r"R7QE-T\d+"
        
        print(f"[DEBUG] Searching for Zephyr key in tags: {tags}")
        
        for tag in tags:
            if re.match(pattern, tag):
                print(f"✓ Found Zephyr key: {tag}")
                return tag
        
        return None
    
    def validate_test_case_exists(self, test_case_key: str) -> bool:
        """
        Validate if test case exists in Zephyr
        
        Args:
            test_case_key: Test case key (e.g., 'R7QE-T4080')
        
        Returns:
            True if test case exists, False otherwise
        """
        try:
            print(f"\n[VALIDATION] Checking if test case '{test_case_key}' exists...")
            endpoint = f"/testcases/{test_case_key}"
            response = self._make_request("GET", endpoint)
            
            if response and "key" in response:
                print(f"✓ Test case '{test_case_key}' exists")
                return True
            else:
                print(f"✗ Test case '{test_case_key}' NOT found")
                return False
        
        except Exception as e:
            print(f"✗ Error validating test case: {e}")
            return False
    
    def validate_test_cycle_exists(self, test_cycle_key: str) -> bool:
        """
        Validate if test cycle exists in Zephyr
        
        Args:
            test_cycle_key: Test cycle key (e.g., 'R7QE-R9')
        
        Returns:
            True if test cycle exists, False otherwise
        """
        try:
            print(f"[VALIDATION] Checking if test cycle '{test_cycle_key}' exists...")
            endpoint = f"/testcycles/{test_cycle_key}"
            response = self._make_request("GET", endpoint)
            
            if response and "key" in response:
                print(f"✓ Test cycle '{test_cycle_key}' exists")
                return True
            else:
                print(f"✗ Test cycle '{test_cycle_key}' NOT found")
                return False
        
        except Exception as e:
            print(f"✗ Error validating test cycle: {e}")
            return False
    
    def validate_folder_exists(self, project_key: str, folder_id: str) -> bool:
        """
        Validate if folder exists in Zephyr project
        
        Args:
            project_key: Jira project key (e.g., 'R7QE')
            folder_id: Folder ID to validate
        
        Returns:
            True if folder exists, False otherwise
        """
        try:
            print(f"[VALIDATION] Checking if folder '{folder_id}' exists in project '{project_key}'...")
            endpoint = f"/testcases?projectKey={project_key}&folderId={folder_id}"
            response = self._make_request("GET", endpoint)
            
            # If we get a response with values array, folder exists
            if response and "values" in response:
                print(f"✓ Folder '{folder_id}' exists in project '{project_key}'")
                return True
            else:
                print(f"✗ Folder '{folder_id}' NOT found in project '{project_key}'")
                return False
        
        except Exception as e:
            print(f"✗ Error validating folder: {e}")
            return False
    
    def validate_all_prerequisites(self, test_case_key: str, test_cycle_key: str, project_key: str, folder_id: str) -> bool:
        """
        Validate all prerequisites before creating execution
        
        Args:
            test_case_key: Test case key
            test_cycle_key: Test cycle key
            project_key: Jira project key
            folder_id: Folder ID
        
        Returns:
            True if all validations pass, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"VALIDATION PHASE: Checking all prerequisites")
        print(f"{'='*60}\n")
        
        # Check test case
        if not self.validate_test_case_exists(test_case_key):
            print(f"✗ VALIDATION FAILED: Test case '{test_case_key}' does not exist")
            return False
        
        # Check test cycle
        if not self.validate_test_cycle_exists(test_cycle_key):
            print(f"✗ VALIDATION FAILED: Test cycle '{test_cycle_key}' does not exist")
            return False
        
        # Check folder
        if not self.validate_folder_exists(project_key, folder_id):
            print(f"✗ VALIDATION FAILED: Folder '{folder_id}' does not exist in project '{project_key}'")
            return False
        
        print(f"\n✓ ALL VALIDATIONS PASSED - Proceeding with execution creation\n")
        return True
    
    def update_zephyr_execution(self, tags: List[str], status: str, project_key: str = "R7QE", test_cycle_key: str = None, folder_id: str = None) -> Dict:
        """
        Update test execution in Zephyr Scale Cloud with validation
        
        Args:
            tags: List of test tags from Robot Framework (should contain Zephyr key)
            status: Test execution status (PASS or FAIL)
            project_key: Jira project key (default: R7QE)
            test_cycle_key: Test cycle key (required for execution creation)
            folder_id: Folder ID for validation
        
        Returns:
            API response dictionary
        """
        print(f"\n{'='*60}")
        print(f"Updating Zephyr Execution")
        print(f"{'='*60}\n")
        
        # Extract Zephyr key from tags
        test_case_key = self.extract_zephyr_key_from_tags(tags)
        
        if not test_case_key:
            error_msg = "ERROR: No Zephyr Key found in tags. Skipping Jira update."
            print(f"✗ {error_msg}")
            return {"error": error_msg}
        
        # Validate test_cycle_key
        if not test_cycle_key:
            error_msg = "ERROR: Test Cycle Key is required. Skipping Jira update."
            print(f"✗ {error_msg}")
            return {"error": error_msg}
        
        # Validate all prerequisites
        if not self.validate_all_prerequisites(test_case_key, test_cycle_key, project_key, folder_id):
            error_msg = "ERROR: Validation failed. Test case, cycle, or folder does not exist."
            return {"error": error_msg}
        
        # Validate status
        status_upper = status.upper()
        valid_statuses = ["PASS", "FAIL"]
        
        if status_upper not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Must be 'PASS' or 'FAIL'")
        
        # Build payload
        endpoint = "/testexecutions"
        payload = {
            "projectKey": project_key,
            "testCaseKey": test_case_key,
            "statusName": status_upper,
            "testCycleKey": test_cycle_key
        }
        
        try:
            print(f"Step 1: Creating test execution for {test_case_key} with status {status_upper} in cycle {test_cycle_key}...")
            response = self._make_request("POST", endpoint, payload)
            print(f"✓ Test execution created successfully\n")
            
            result = {
                "testCaseKey": test_case_key,
                "executionStatus": status_upper,
                "projectKey": project_key,
                "testCycleKey": test_cycle_key,
                "executionDetails": response
            }
            
            print(f"{'='*60}")
            print(f"Update Result: {result['testCaseKey']} - {result['executionStatus']}")
            print(f"{'='*60}\n")
            
            return result
        
        except Exception as e:
            print(f"✗ Error updating test execution: {e}")
            raise
    
    # Robot Framework Keyword
    def sync_result(self, tags, status, project_key="R7QE", test_cycle_key=None, folder_id=None, bearer_token=None):
        """
        KEYWORD: Sync Result
        
        Validates prerequisites and updates test execution in Zephyr Scale Cloud
        
        Args:
            tags: Test tags (should contain Zephyr key like R7QE-T4080)
            status: Test execution status (PASS or FAIL)
            project_key: Jira project key (default: R7QE)
            test_cycle_key: Test cycle key (required)
            folder_id: Folder ID (required for validation)
            bearer_token: Custom bearer token (optional)
        
        Returns:
            Success or error message
        """
        try:
            zephyr = ZephyrSync(bearer_token=bearer_token)
            
            # Convert tags to list if it's a string
            if isinstance(tags, str):
                tags_list = [tags]
            else:
                tags_list = list(tags) if hasattr(tags, '__iter__') else [tags]
            
            result = zephyr.update_zephyr_execution(tags_list, status, project_key, test_cycle_key, folder_id)
            
            if "error" in result:
                return f"⚠ {result['error']}"
            
            return f"✓ Success: {result['testCaseKey']} updated with status {result['executionStatus']}"
        
        except Exception as e:
            error_msg = f"✗ Error updating test execution: {str(e)}"
            print(error_msg)
            return error_msg