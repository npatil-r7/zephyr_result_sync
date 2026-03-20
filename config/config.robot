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
# ZEPHYR CONFIGURATION (Legacy - Now handled by Environment Variables)
# ============================================================================
# These variables are kept for reference only.
# The ZephyrListener now uses environment variables instead:
#
# Required Environment Variables:
#   ZEPHYR_API_KEY       - Zephyr Scale API Bearer Token
#   ZEPHYR_PROJECT_KEY   - Jira Project Key (e.g., R7QE)
#
# Optional Environment Variables:
#   ZEPHYR_BASE_URL      - API Base URL
#                          EU: https://eu.api.zephyrscale.smartbear.com/v2
#                          US: https://api.zephyrscale.smartbear.com/v2
#   ZEPHYR_FOLDER_ID     - Test Cycle Folder ID
#                          This is the folder where new Test Cycles will be created.
#                          To find Folder ID: Zephyr Scale → Test Cycles → Click folder → Check URL
#                          Example: 450085
#
# ${SYNC_TO_ZEPHYR}    ${True}
# ${PROJECT_KEY}       R7QE
# ${FOLDER_ID}         450085    # Test Cycle Folder ID
# ${TEST_CYCLE}        R7QE-R9   # Auto-created by listener now

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
${LOG_LEVEL}         INFO