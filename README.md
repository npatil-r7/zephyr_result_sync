# 🚀 Zephyr Scale - Robot Framework Listener

Automatically sync your Robot Framework test results to Zephyr Scale Cloud.

---

## 📦 Installation

Add this to your `requirements.txt`:

```text
git+https://github.com/npatil-r7/zephyr_result_sync.git
```

Then install:

```bash
pip install -r requirements.txt
```

---

## ⚡ Quick Start

### 1. Set Environment Variables

```bash
# Required
export ZEPHYR_API_KEY="your_api_token"
export ZEPHYR_PROJECT_KEY="R7QE"

# Optional
export ZEPHYR_BASE_URL="https://eu.api.zephyrscale.smartbear.com/v2"
export ZEPHYR_FOLDER_ID="450085"
```

| Variable | Required | Description |
|----------|----------|-------------|
| `ZEPHYR_API_KEY` | ✅ Yes | Zephyr Scale API token |
| `ZEPHYR_PROJECT_KEY` | ✅ Yes | Jira project key (e.g., `R7QE`) |
| `ZEPHYR_BASE_URL` | ❌ No | API URL (defaults to EU region) |
| `ZEPHYR_FOLDER_ID` | ❌ No | Folder ID for Test Cycles |

#### 🔑 How to Get API Token

1. Jira → Your Project → **Zephyr Scale**
2. **Settings** ⚙️ → **API Access Tokens**
3. **Create Access Token** → Copy

#### 📂 How to Find Folder ID

1. Jira → Your Project → **Zephyr Scale** → **Test Cycles**
2. Click on your folder
3. Check URL: `...?folderId=450085`

---

### 2. Tag Your Tests

```robot
*** Test Cases ***
Login Valid User
    [Tags]    R7QE-T4080
    Log    This test will sync to Zephyr

Login Invalid User
    [Tags]    R7QE-T4081    smoke    regression
    Log    Multiple tags allowed, one must be Zephyr key
```

**Tag Format:** `{PROJECT_KEY}-T{NUMBER}`

| Example | Valid? |
|---------|--------|
| `R7QE-T4080` | ✅ Yes |
| `R7QE-4080` | ❌ No (missing `T`) |
| `T4080` | ❌ No (missing project key) |

---

### 3. Run Tests

```bash
robot --listener ZephyrListener tests/
```

---

## 🔧 Auto-Enable Listener (Optional)

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

## 💻 Console Output

```
======================================================================
🚀 [ZEPHYR] Initializing Zephyr Scale Listener...
======================================================================
✅ [ZEPHYR] Configuration loaded successfully
   📍 Base URL: https://eu.api.zephyrscale.smartbear.com/v2
   📁 Project Key: R7QE
   📂 Folder ID: 450085
======================================================================

📋 [ZEPHYR] Creating Test Cycle: TestCycle 20th Mar 2026 2:30 PM
✅ [ZEPHYR] Test Cycle created: R7QE-R15

🔄 [ZEPHYR] Syncing: R7QE-T4080 (Login Valid User)
✅ [ZEPHYR] Synced: R7QE-T4080 → Pass

🔄 [ZEPHYR] Syncing: R7QE-T4081 (Login Invalid User)
❌ [ZEPHYR] Synced: R7QE-T4081 → Fail

======================================================================
📊 [ZEPHYR] Sync Summary
======================================================================
   📋 Test Cycle: R7QE-R15
   ✅ Synced:  2
   ⚠️  Skipped: 0
   ❌ Failed:  0
======================================================================
```

---

## 📋 Methods Reference

| Method | Purpose |
|--------|---------|
| `__init__()` | Load configuration from environment variables |
| `_validate_configuration()` | Check required env vars are set |
| `_get_ist_timestamp()` | Generate IST timestamp for Test Cycle name |
| `_get_iso_timestamp()` | Generate ISO timestamp for API calls |
| `_make_request()` | HTTP request handler with error handling |
| `_extract_test_case_key()` | Extract Zephyr key from test tags |
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

## ❓ Troubleshooting

| Error | Solution |
|-------|----------|
| `Missing required environment variables` | Set `ZEPHYR_API_KEY` and `ZEPHYR_PROJECT_KEY` |
| `401 Unauthorized` | Generate new API token from Zephyr Scale settings |
| `No Jira Key found for test` | Add `[Tags]    R7QE-T1234` to your test |
| `ModuleNotFoundError: ZephyrListener` | Run `pip install -r requirements.txt` |

---

## 👤 Author

**Nileshkumar Patil**

---

## 📄 License

MIT License
