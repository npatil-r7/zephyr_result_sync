# Zephyr Scale - Robot Framework Integration

A POC (Proof of Concept) project demonstrating automated test execution with Robot Framework and automatic synchronization of test results to Zephyr Scale Cloud.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)ß
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Flow Diagram](#flow-diagram)
- [Methods Reference](#methods-reference)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project automates:
1. **Web UI Testing** - Using Robot Framework + SeleniumLibrary
2. **Zephyr Sync** - Automatically syncs test results (PASS/FAIL) to Zephyr Scale Cloud
3. **Validation** - Validates test case, test cycle, and folder exist before execution

### Key Features

| Feature | Description |
|---------|-------------|
| ✅ Tag-based sync | Uses test tags (e.g., `R7QE-T4080`) to identify Zephyr test cases |
| ✅ Pre-validation | Validates test case, cycle, and folder exist before creating execution |
| ✅ Auto status sync | Automatically syncs PASS/FAIL status to Zephyr |
| ✅ Configurable | Easy to enable/disable Zephyr sync via config |

---

## 📁 Project Structure

```
/POC_ Zephyr/
├── config/
│   └── config.robot          # All configuration variables
├── libraries/
│   └── ZephyrSync.py         # Zephyr Scale API integration
├── tests/
│   └── login_poc.robot       # Test cases
├── results/                  # Test execution results (auto-generated)
│   ├── log.html
│   ├── report.html
│   └── output.xml
└── README.md                 # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `config/config.robot` | Contains all configuration variables (URLs, credentials, Zephyr settings) |
| `libraries/ZephyrSync.py` | Python library for Zephyr Scale Cloud API integration |
| `tests/login_poc.robot` | Robot Framework test cases with Zephyr tags |
| `results/` | Auto-generated folder containing test execution reports |

---

## 🔧 Prerequisites

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.8+ | Runtime environment |
| Robot Framework | 6.0+ | Test automation framework |
| Chrome Browser | Latest | Browser for UI testing |
| ChromeDriver | Matching Chrome version | Selenium WebDriver |

### Accounts Required

| Account | Purpose |
|---------|---------|
| Jira Cloud | Project management |
| Zephyr Scale Cloud | Test management |

---

## 📦 Installation Guide

### Step 1: Clone/Create Project

```bash
mkdir -p /Users/npatil/Work/POC_\ Zephyr
cd /Users/npatil/Work/POC_\ Zephyr
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check Robot Framework
robot --version

# Check Python packages
pip list | grep -E "robotframework|requests"
```

### Step 5: Create Folder Structure

```bash
mkdir -p config libraries tests results
```
ß
---

## ⚙️ Configuration

### config/config.robot

```robot
*** Variables ***
# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================
${LOGIN_URL}         https://www.saucedemo.com/
${BROWSER}           Chrome

# ============================================================================
# USER CREDENTIALS
# ============================================================================
${USERNAME}          standard_user
${PASSWORD}          secret_sauce

# ============================================================================
# ZEPHYR CONFIGURATION
# ============================================================================
${SYNC_TO_ZEPHYR}    ${True}
${PROJECT_KEY}       R7QE
${FOLDER_ID}         420067
${TEST_CYCLE}        R7QE-R9
```

### Configuration Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `${LOGIN_URL}` | Application URL to test | `https://www.saucedemo.com/` |
| `${BROWSER}` | Browser to use | `Chrome` |
| `${USERNAME}` | Test user username | `standard_user` |
| `${PASSWORD}` | Test user password | `secret_sauce` |
| `${SYNC_TO_ZEPHYR}` | Enable/disable Zephyr sync | `${True}` or `${False}` |
| `${PROJECT_KEY}` | Jira project key | `R7QE` |
| `${FOLDER_ID}` | Zephyr test folder ID | `420067` |
| `${TEST_CYCLE}` | Zephyr test cycle key | `R7QE-R9` |

### Zephyr Bearer Token

The Bearer token is stored in `libraries/ZephyrSync.py`:

```python
BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

> ⚠️ **Security Note:** In production, use environment variables instead of hardcoding tokens.

---

## 🚀 Usage

### Run All Tests

```bash
cd /Users/npatil/Work/POC_\ Zephyr
robot tests/login_poc.robot
```

### Run with Output Directory

```bash
robot --outputdir results tests/login_poc.robot
```

### Run Specific Test

```bash
robot --test "Login Valid User" tests/login_poc.robot
```

### Run by Tag

```bash
robot --include R7QE-T4080 tests/login_poc.robot
```

### Disable Zephyr Sync

Edit `config/config.robot`:
```robot
${SYNC_TO_ZEPHYR}    ${False}
```

---

## 🔌 API Reference

### Zephyr Scale Cloud APIs Used

| # | API | Method | Purpose |
|---|-----|--------|---------|
| 1 | `/testcases/{key}` | GET | Validate test case exists |
| 2 | `/testcycles/{key}` | GET | Validate test cycle exists |
| 3 | `/testcases?projectKey={key}&folderId={id}` | GET | Validate folder exists |
| 4 | `/testexecutions` | POST | Create test execution |

### API Base URL

```
https://eu.api.zephyrscale.smartbear.com/v2
```

### Example API Calls (curl)

**1. Validate Test Case:**
```bash
curl -X GET "https://eu.api.zephyrscale.smartbear.com/v2/testcases/R7QE-T4080" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**2. Validate Test Cycle:**
```bash
curl -X GET "https://eu.api.zephyrscale.smartbear.com/v2/testcycles/R7QE-R9" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**3. Create Test Execution:**
```bash
curl -X POST "https://eu.api.zephyrscale.smartbear.com/v2/testexecutions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "projectKey": "R7QE",
    "testCaseKey": "R7QE-T4080",
    "statusName": "PASS",
    "testCycleKey": "R7QE-R9"
  }'
```

**4. Get Executions by Test Case:**
```bash
curl -X GET "https://eu.api.zephyrscale.smartbear.com/v2/testexecutions?testCaseKey=R7QE-T4080" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**5. Get Executions by Test Cycle:**
```bash
curl -X GET "https://eu.api.zephyrscale.smartbear.com/v2/testexecutions?testCycleKey=R7QE-R9" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 📊 Flow Diagram

### Test Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROBOT FRAMEWORK TEST                         │
│                                                                 │
│  ┌─────────────────┐                                            │
│  │  Test Case      │                                            │
│  │  [Tags] R7QE-T4080                                           │
│  └────────┬────────┘                                            │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │  Test Executes  │                                            │
│  │  (PASS/FAIL)    │                                            │
│  └────────┬────────┘                                            │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │  Test Teardown  │                                            │
│  │  Sync Zephyr    │                                            │
│  └────────┬────────┘                                            │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ZEPHYR SYNC LIBRARY                          │
│                                                                 │
│  ┌─────────────────┐                                            │
│  │  sync_result()  │  ← Entry Point                             │
│  └────────┬────────┘                                            │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────┐                                │
│  │  extract_zephyr_key_from_tags()                              │
│  │  Tags: ['R7QE-T4080']                                        │
│  │  Returns: 'R7QE-T4080'                                       │
│  └────────┬────────────────────┘                                │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────┐                                │
│  │  validate_all_prerequisites()                                │
│  │  ├── validate_test_case_exists()    → GET /testcases/{key}   │
│  │  ├── validate_test_cycle_exists()   → GET /testcycles/{key}  │
│  │  └── validate_folder_exists()       → GET /testcases?...     │
│  └────────┬────────────────────┘                                │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────┐                                │
│  │  update_zephyr_execution()  │                                │
│  │  POST /testexecutions       │                                │
│  │  {                          │                                │
│  │    "projectKey": "R7QE",    │                                │
│  │    "testCaseKey": "R7QE-T4080",                              │
│  │    "statusName": "PASS",    │                                │
│  │    "testCycleKey": "R7QE-R9"│                                │
│  │  }                          │                                │
│  └────────┬────────────────────┘                                │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ZEPHYR SCALE CLOUD                           │
│                                                                 │
│  Test Cycle: R7QE-R9                                            │
│  ├── R7QE-T4080 (Login Valid User)     → PASS ✅                │
│  └── R7QE-T4081 (Login Invalid Password) → FAIL ❌              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Methods Reference

### ZephyrSync.py Methods

| # | Method | Purpose | Used? |
|---|--------|---------|-------|
| 1 | `__init__(bearer_token)` | Initialize API with bearer token and headers | ✅ Yes |
| 2 | `_make_request(method, endpoint, data)` | Make HTTP requests (GET/POST/PUT) to Zephyr API | ✅ Yes |
| 3 | `extract_zephyr_key_from_tags(tags)` | Extract test case key (R7QE-T4080) from tags | ✅ Yes |
| 4 | `validate_test_case_exists(test_case_key)` | Check if test case exists in Zephyr | ✅ Yes |
| 5 | `validate_test_cycle_exists(test_cycle_key)` | Check if test cycle exists in Zephyr | ✅ Yes |
| 6 | `validate_folder_exists(project_key, folder_id)` | Check if folder exists in project | ✅ Yes |
| 7 | `validate_all_prerequisites(...)` | Validate all 3 (test case, cycle, folder) together | ✅ Yes |
| 8 | `update_zephyr_execution(...)` | Create test execution in Zephyr | ✅ Yes |
| 9 | `sync_result(...)` | **Robot Framework Keyword** - Main entry point | ✅ Yes |

### Method Details

#### 1. `__init__(bearer_token)`
```python
def __init__(self, bearer_token: str = None):
```
- Initializes Zephyr API connection
- Sets up headers with Bearer token
- Uses default token if none provided

#### 2. `_make_request(method, endpoint, data)`
```python
def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
```
- Internal method for HTTP requests
- Supports GET, POST, PUT methods
- Handles errors and response parsing
- Returns JSON response as dictionary

#### 3. `extract_zephyr_key_from_tags(tags)`
```python
def extract_zephyr_key_from_tags(self, tags: List[str]) -> Optional[str]:
```
- Searches tags for pattern `R7QE-T\d+`
- Returns test case key like `R7QE-T4080`
- Returns None if no match found

#### 4. `validate_test_case_exists(test_case_key)`
```python
def validate_test_case_exists(self, test_case_key: str) -> bool:
```
- API: `GET /testcases/{test_case_key}`
- Returns True if test case exists
- Returns False if not found or error

#### 5. `validate_test_cycle_exists(test_cycle_key)`
```python
def validate_test_cycle_exists(self, test_cycle_key: str) -> bool:
```
- API: `GET /testcycles/{test_cycle_key}`
- Returns True if test cycle exists
- Returns False if not found or error

#### 6. `validate_folder_exists(project_key, folder_id)`
```python
def validate_folder_exists(self, project_key: str, folder_id: str) -> bool:
```
- API: `GET /testcases?projectKey={project_key}&folderId={folder_id}`
- Returns True if folder exists
- Returns False if not found or error

#### 7. `validate_all_prerequisites(...)`
```python
def validate_all_prerequisites(self, test_case_key: str, test_cycle_key: str, project_key: str, folder_id: str) -> bool:
```
- Calls all 3 validation methods
- Returns True only if ALL validations pass
- Prints detailed validation status

#### 8. `update_zephyr_execution(...)`
```python
def update_zephyr_execution(self, tags: List[str], status: str, project_key: str = "R7QE", test_cycle_key: str = None, folder_id: str = None) -> Dict:
```
- API: `POST /testexecutions`
- Creates test execution with PASS/FAIL status
- Returns execution details dictionary

#### 9. `sync_result(...)` ⭐ Main Entry Point
```python
def sync_result(self, tags, status, project_key="R7QE", test_cycle_key=None, folder_id=None, bearer_token=None):
```
- **Robot Framework Keyword**
- Called from test teardown
- Orchestrates the entire sync flow
- Returns success or error message

---

## 🐛 Troubleshooting

### Common Issues

#### 1. ChromeDriver Version Mismatch
```
Error: session not created: This version of ChromeDriver only supports Chrome version XX
```
**Solution:**
```bash
# Check Chrome version
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Download matching ChromeDriver
brew upgrade chromedriver
```

#### 2. 401 Unauthorized Error
```
✗ ERROR: 401 Unauthorized - Token is invalid or expired
```
**Solution:**
- Check Bearer token is valid
- Generate new token from Zephyr Scale settings

#### 3. Test Case Not Found
```
✗ VALIDATION FAILED: Test case 'R7QE-T4080' does not exist
```
**Solution:**
- Verify test case exists in Zephyr Scale
- Check project key is correct
- Ensure tag matches exact test case key

#### 4. Test Cycle Not Found
```
✗ VALIDATION FAILED: Test cycle 'R7QE-R9' does not exist
```
**Solution:**
- Create test cycle in Zephyr Scale
- Verify test cycle key is correct

#### 5. Module Not Found
```
ModuleNotFoundError: No module named 'requests'
```
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📝 Test Case Naming Convention

### Tags Format
```robot
[Tags]    R7QE-T4080
```

Where:
- `R7QE` = Project Key
- `T` = Test case identifier
- `4080` = Test case number

### Example
```robot
*** Test Cases ***
Login Valid User
    [Tags]    R7QE-T4080
    [Documentation]    Test login with valid credentials
    # Test steps here
```

---

## 👤 Author

**Nileshkumar Patil**

---

## 📄 License

This project is for internal POC purposes.

---

## 🔗 References

- [Robot Framework Documentation](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
- [SeleniumLibrary Documentation](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html)
- [Zephyr Scale Cloud API Documentation](https://support.smartbear.com/zephyr-scale-cloud/api-docs/)
- [SauceDemo Test Site](https://www.saucedemo.com/)