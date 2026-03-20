# 🚀 Zephyr Scale - Robot Framework Listener

Automatically sync your Robot Framework test results to Zephyr Scale Cloud. No manual work needed!

---

## ⚡ 3-Step Setup

### Step 1: Install

```bash
pip install git+https://github.com/npatil-r7/zephyr-robotframework-listener.git
```

### Step 2: Set Environment Variables

```bash
export ZEPHYR_API_KEY="your_token"
export ZEPHYR_PROJECT_KEY="R7QE"
export ZEPHYR_BASE_URL="https://eu.api.zephyrscale.smartbear.com/v2"
export ZEPHYR_FOLDER_ID="your_test_cycle_folder_id"
```

### Step 3: Run Tests

```bash
robot --listener ZephyrListener tests/
```

**Done!** ✅ Your results are now syncing to Zephyr Scale.

---

## 📋 Complete Setup Guide

### 1. Installation Options

| Method | Command |
|--------|---------|
| **From GitHub** | `pip install git+https://github.com/npatil-r7/zephyr-robotframework-listener.git` |
| **From Source** | `git clone <repo> && cd <repo> && pip install .` |
| **Development** | `pip install -e .` |

---

### 2. Environment Variables

Copy and paste these commands in your terminal:

```bash
# =============================================
# REQUIRED (Must Set)
# =============================================

# Your Zephyr API Token
export ZEPHYR_API_KEY="paste_your_token_here"

# Your Jira Project Key (e.g., R7QE, PROJ, TEST)
export ZEPHYR_PROJECT_KEY="R7QE"

# =============================================
# OPTIONAL (Has Defaults)
# =============================================

# API URL - Only change if you're in US region
# EU (Default): https://eu.api.zephyrscale.smartbear.com/v2
# US:           https://api.zephyrscale.smartbear.com/v2
export ZEPHYR_BASE_URL="https://eu.api.zephyrscale.smartbear.com/v2"

# Folder ID - Where to create Test Cycles
# Leave empty to create at root level
export ZEPHYR_FOLDER_ID="450085"
```

#### 🔑 How to Get Your API Token

1. Open Jira → Go to your project
2. Click **Zephyr Scale** (in the menu)
3. Click **Settings** ⚙️ → **API Access Tokens**
4. Click **Create Access Token**
5. Copy the token

#### 📂 How to Find Folder ID

1. Open Jira → Go to your project
2. Click **Zephyr Scale** → **Test Cycles**
3. Click on the folder you want
4. Look at the URL: `...?folderId=450085`
5. Use that number as `ZEPHYR_FOLDER_ID`

---

## 🏷️ Tag Handling (Important!)

### ⚠️ Tags Are Required

Every test **MUST** have a Zephyr test case tag. Tests without proper tags will be **skipped** from syncing.

### Tag Format

```
{PROJECT_KEY}-T{NUMBER}
```

| Example | Valid? |
|---------|--------|
| `R7QE-T4080` | ✅ Yes |
| `PROJ-T123` | ✅ Yes |
| `TEST-T999` | ✅ Yes |
| `R7QE-4080` | ❌ No (missing `T`) |
| `T4080` | ❌ No (missing project key) |
| `smoke` | ❌ No (not a Zephyr key) |

### How to Tag Your Tests

```robot
*** Test Cases ***
Login Should Work
    [Tags]    R7QE-T4080
    # Your test steps here

Login Should Fail With Wrong Password
    [Tags]    R7QE-T4081    smoke    regression
    # You can have multiple tags, but one MUST be Zephyr key
```

### How Tag Extraction Works

The listener scans all tags for a pattern matching `{PROJECT_KEY}-T\d+`:

```
Test Tags: ['R7QE-T4080', 'smoke', 'regression']
                 ↓
Pattern Match: R7QE-T4080 ✅ Found!
                 ↓
Sync to Zephyr: R7QE-T4080 → Pass/Fail
```

### What Happens Without Tags?

| Scenario | Behavior | Console Output |
|----------|----------|----------------|
| ✅ Has Zephyr tag | Syncs to Zephyr | `✅ Synced: R7QE-T4080 → Pass` |
| ⚠️ No Zephyr tag | **Skipped** (not synced) | `⚠️ Skipping: No Jira Key found` |
| ⚠️ Wrong format | **Skipped** (not synced) | `⚠️ Skipping: No Jira Key found` |

### Console Output for Missing Tags

```
⚠️ [ZEPHYR] Skipping: No Jira Key found for test 'My Untagged Test'
   Tags found: ['smoke', 'regression']
   Expected pattern: R7QE-T<number>
```

### Best Practices for Tags

```robot
*** Test Cases ***
# ✅ GOOD - Has Zephyr tag
Login Valid User
    [Tags]    R7QE-T4080
    Log    This will sync to Zephyr

# ✅ GOOD - Multiple tags including Zephyr tag
Login Invalid User
    [Tags]    R7QE-T4081    smoke    critical
    Log    This will sync to Zephyr (uses R7QE-T4081)

# ❌ BAD - No Zephyr tag
Checkout Flow
    [Tags]    smoke    e2e
    Log    This will NOT sync (no R7QE-T tag)

# ❌ BAD - Wrong format
Payment Test
    [Tags]    T4082    regression
    Log    This will NOT sync (missing project key)
```

---

### 3. Run Your Tests

```bash
robot --listener ZephyrListener --outputdir results tests/
```

---

## 💻 What You'll See

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

🔄 [ZEPHYR] Syncing: R7QE-T4080 (Login Should Work)
✅ [ZEPHYR] Synced: R7QE-T4080 → Pass

🔄 [ZEPHYR] Syncing: R7QE-T4081 (Login Should Fail)
❌ [ZEPHYR] Synced: R7QE-T4081 → Fail

⚠️ [ZEPHYR] Skipping: No Jira Key found for test 'Untagged Test'
   Tags found: ['smoke', 'regression']
   Expected pattern: R7QE-T<number>

======================================================================
📊 [ZEPHYR] Sync Summary
======================================================================
   📋 Test Cycle: R7QE-R15
   ✅ Synced:  2
   ⚠️  Skipped: 1
   ❌ Failed:  0
   📈 Total:   3
======================================================================
```

---

## 🔧 CI/CD Setup

### GitHub Actions

```yaml
name: Run Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install
        run: |
          pip install -r requirements.txt
          pip install git+https://github.com/npatil-r7/zephyr-robotframework-listener.git
      
      - name: Run Tests
        env:
          ZEPHYR_API_KEY: ${{ secrets.ZEPHYR_API_KEY }}
          ZEPHYR_PROJECT_KEY: R7QE
          ZEPHYR_FOLDER_ID: "450085"
        run: robot --listener ZephyrListener --outputdir results tests/
```

### Jenkins

```groovy
pipeline {
    agent any
    
    environment {
        ZEPHYR_API_KEY     = credentials('zephyr-api-key')
        ZEPHYR_PROJECT_KEY = 'R7QE'
        ZEPHYR_FOLDER_ID   = '450085'
    }
    
    stages {
        stage('Test') {
            steps {
                sh 'pip install git+https://github.com/npatil-r7/zephyr-robotframework-listener.git'
                sh 'robot --listener ZephyrListener --outputdir results tests/'
            }
        }
    }
}
```

---

## ❓ Troubleshooting

### ❌ "Missing required environment variables"

```bash
# You forgot to set the variables. Run:
export ZEPHYR_API_KEY="your_token"
export ZEPHYR_PROJECT_KEY="R7QE"
export ZEPHYR_BASE_URL="https://eu.api.zephyrscale.smartbear.com/v2"
export ZEPHYR_FOLDER_ID="your_test_cycle_folder_id"
```

### ❌ "401 Unauthorized"

Your API token is invalid or expired. Generate a new one from Zephyr Scale settings.

### ⚠️ "No Jira Key found for test"

Add the Zephyr tag to your test:

```robot
*** Test Cases ***
My Test
    [Tags]    R7QE-T1234    # ← Add this (must match PROJECT_KEY-T<number>)
    # test steps
```

**Common mistakes:**
- ❌ `[Tags]    T1234` - Missing project key
- ❌ `[Tags]    R7QE-1234` - Missing `T`
- ❌ `[Tags]    smoke` - Not a Zephyr key
- ✅ `[Tags]    R7QE-T1234` - Correct!

### ❌ "ModuleNotFoundError: No module named 'ZephyrListener'"

```bash
# Install the package:
pip install git+https://github.com/npatil-r7/zephyr-robotframework-listener.git

# Or if running locally:
pip install -e .
```

---

## 📊 Quick Reference

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ZEPHYR_API_KEY` | ✅ Yes | Your Zephyr API token |
| `ZEPHYR_PROJECT_KEY` | ✅ Yes | Jira project key (e.g., `R7QE`) |
| `ZEPHYR_BASE_URL` | ❌ No | API URL (defaults to EU) |
| `ZEPHYR_FOLDER_ID` | ❌ No | Folder for Test Cycles |

### API Regions

| Region | Base URL |
|--------|----------|
| EU (Default) | `https://eu.api.zephyrscale.smartbear.com/v2` |
| US | `https://api.zephyrscale.smartbear.com/v2` |

### Tag Format

| Pattern | Example | Description |
|---------|---------|-------------|
| `{PROJECT_KEY}-T{NUMBER}` | `R7QE-T4080` | Valid Zephyr test case key |

---

## 🎯 Features

- ✅ **Zero Config Tests** - Just add tags, no teardown code needed
- ✅ **Auto Test Cycle** - Creates `TestCycle 20th Mar 2026 2:30 PM` automatically
- ✅ **Smart Tag Detection** - Automatically finds Zephyr keys in tags
- ✅ **Skip Warnings** - Clearly shows which tests are missing tags
- ✅ **Fail-Safe** - API errors won't break your test run
- ✅ **Clear Logs** - Emoji feedback shows what's happening
- ✅ **CI/CD Ready** - Works with GitHub Actions, Jenkins, GitLab

---

## 🔄 Sync Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Test: "Login Valid User"                                   │
│  Tags: ['R7QE-T4080', 'smoke', 'regression']                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  🔍 Tag Extraction                                          │
│  Pattern: R7QE-T\d+                                         │
│  Match: R7QE-T4080 ✅                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  📤 POST /testexecutions                                    │
│  {                                                          │
│    "projectKey": "R7QE",                                    │
│    "testCaseKey": "R7QE-T4080",                             │
│    "testCycleKey": "R7QE-R15",                              │
│    "statusName": "Pass"                                     │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ✅ Synced: R7QE-T4080 → Pass                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📞 Support

**Author:** Nileshkumar Patil

**Issues:** [GitHub Issues](https://github.com/npatil-r7/zephyr-robotframework-listener/issues)

---

## 📄 License

MIT License
