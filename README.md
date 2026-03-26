# 🚀 Zephyr Scale - Robot Framework Listener

Automatically sync your Robot Framework test results to Zephyr Scale Cloud.

---

## 📦 Installation

```bash
pip install git+https://github.com/npatil-r7/zephyr_result_sync.git
```

---

## ⚡ Quick Start

### 1. Set Environment Variables

```bash
export ZEPHYR_API_KEY="your_api_token"
export ZEPHYR_PROJECT_KEY="PROJECT_KEY"
export ZEPHYR_BASE_URL="https://eu.api.zephyrscale.smartbear.com/v2"
export ZEPHYR_FOLDER_ID="YOUR_FOLDER_ID"
```

| Variable | Required | Description |
|----------|----------|-------------|
| `ZEPHYR_API_KEY` | ✅ Yes | Zephyr Scale API token |
| `ZEPHYR_PROJECT_KEY` | ✅ Yes | Jira project key (e.g., `R7QE`) |
| `ZEPHYR_BASE_URL` | ❌ No | API URL (defaults to EU region) |
| `ZEPHYR_FOLDER_ID` | ❌ No | Folder ID for Test Cycles |

### 2. Tag Your Tests

```robot
*** Test Cases ***
Login Valid User
    [Tags]    R7QE-T4080
    Log    This test will sync to Zephyr

Login Invalid User
    [Tags]    R7QE-T4081
    Log    This test will also sync
```

**Tag Format:** `{PROJECT_KEY}-T{NUMBER}` (e.g., `R7QE-T4080`)

### 3. Run Tests

```bash
robot --listener zephyr_listener.ZephyrListener tests/login_poc.robot
```

---

## 🔧 Optional: Auto-Enable Listener

Create `robot.toml` in your project root:

```toml
[robot]
listener = ["ZephyrListener"]
outputdir = "results"
```

Now just run:

```bash
robot tests/
```

---

## 📋 Methods Reference

| Method | Purpose |
|--------|---------|
| `__init__()` | Load configuration from environment variables |
| `_validate_configuration()` | Check required env vars are set |
| `_get_ist_timestamp()` | Generate IST timestamp for Test Cycle name (e.g., `TestCycle 20th Mar 2026 2:30 PM`) |
| `_get_iso_timestamp()` | Generate ISO timestamp for API calls |
| `_make_request()` | HTTP request handler with error handling |
| `_extract_test_case_key()` | Extract Zephyr key from test tags (e.g., `R7QE-T4080`) |
| `start_suite()` | Creates Test Cycle when suite starts |
| `end_test()` | Syncs test result when test ends |
| `end_suite()` | Prints sync summary when suite ends |
| `_create_test_cycle()` | API call to create Test Cycle |
| `_sync_test_result()` | API call to sync test execution |
| `_print_summary()` | Print final sync statistics |

---

## 🔄 Execution Flow

```
Suite Start
    └── _create_test_cycle() → Creates "TestCycle 20th Mar 2026 2:30 PM"

Test End (for each test)
    ├── _extract_test_case_key() → Gets R7QE-T4080 from tags
    └── _sync_test_result() → Syncs Pass/Fail to Zephyr

Suite End
    └── _print_summary() → Shows sync statistics
```

---

## 👤 Author

**Nileshkumar Patil**