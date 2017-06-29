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
    [Arguments]  ${username}  ${password}
    go to  ${LOG_IN_PAGE}
    wait until element is enabled  wp-submit
    sleep  3
    input text  user_login  ${username}
    input text  user_pass  ${password}
    click button  wp-submit

Log Out
    mouse over  //*[@id="wp-admin-bar-my-account"]/a/span
    wait until page contains  Log Out
    click link  Log Out