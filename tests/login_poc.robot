*** Settings ***
Library    SeleniumLibrary
Resource   ../config/config.robot
Test Teardown    Close All Browsers

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
    Fail    This test intentionally fails to demonstrate FAIL status sync

*** Keywords ***
Open Browser With Custom Chrome Options
    [Documentation]    Open browser with Chrome options to disable password manager popup
    ${chrome_options}=    Evaluate    selenium.webdriver.ChromeOptions()
    ${prefs}=    Create Dictionary    
    ...    credentials_enable_service=${False}
    ...    profile.password_manager_enabled=${False}
    Call Method    ${chrome_options}    add_experimental_option    prefs    ${prefs}
    Open Browser    ${LOGIN_URL}    ${BROWSER}    options=${chrome_options}