*** Settings ***
Library    SeleniumLibrary
Library    ../libraries/ZephyrSync.py
Resource   ../config/config.robot
Test Teardown    Sync Zephyr Result If Enabled

*** Test Cases ***
Login Valid User
    [Tags]    R7QE-T4080
    [Documentation]    Test login with valid credentials on SauceDemo
    Open Browser With Custom Chrome Options
    Input Text    id:user-name    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Click Button    id:login-button
    Wait Until Page Contains    Products

Login Invalid Password
    [Tags]    R7QE-T4081
    [Documentation]    Test login with invalid password on SauceDemo
    Open Browser With Custom Chrome Options
    Input Text    id:user-name    ${USERNAME}
    Input Text    id:password    invalidpassword
    Click Button    id:login-button
    Wait Until Page Contains    Epic sadface
    Fail    Login test failed as expected

*** Keywords ***
Sync Zephyr Result If Enabled
    [Documentation]    Sync test result to Zephyr in teardown
    Log    Test Status: ${TEST_STATUS}
    Log    Test Tags: ${TEST_TAGS}
    
    # Convert TEST_STATUS to PASS/FAIL format expected by Zephyr
    ${zephyr_status}=    Set Variable If    '${TEST_STATUS}' == 'PASS'    PASS    FAIL
    
    Run Keyword If    ${SYNC_TO_ZEPHYR}    Sync Result    ${TEST_TAGS}    ${zephyr_status}    ${PROJECT_KEY}    ${TEST_CYCLE}    ${FOLDER_ID}
    Close All Browsers

Open Browser With Custom Chrome Options
    [Documentation]    Open browser with Chrome options to disable password manager popup
    ${chrome_options}=    Evaluate    selenium.webdriver.ChromeOptions()
    ${prefs}=    Create Dictionary    
    ...    credentials_enable_service=${False}
    ...    profile.password_manager_enabled=${False}
    Call Method    ${chrome_options}    add_experimental_option    prefs    ${prefs}
    Open Browser    ${LOGIN_URL}    ${BROWSER}    options=${chrome_options}