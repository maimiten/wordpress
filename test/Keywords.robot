#*** Settings ***
#Library  Selenium2Library
#Resource  Variables.robot

*** Keywords ***
Begin Web Case
    Set Selenium Speed  .5 seconds
    open browser  about:blank  chrome
    maximize browser window

End Web Case
    close browser

Log In
    [Arguments]  ${username}  ${password}  ${url}=${LOG_IN_PAGE}
    go to  ${url}
    wait until element is enabled  //*[@type="submit"]
    sleep  3
    input text  //*[@type="text"]  ${username}
    input text  //*[@type="password"]  ${password}
    click button  //*[@type="submit"]

Log Out
    mouse over  //*[@id="wp-admin-bar-my-account"]/a/span
    wait until page contains  Log Out
    click link  Log Out