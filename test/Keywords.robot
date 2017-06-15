*** Keywords ***
Begin Web Case
    Set Selenium Speed  .5 seconds
    open browser  about:blank  chrome
    maximize browser window

End Web Case
    close browser

Log In
    go to  ${LOG_IN_PAGE}
    wait until element is enabled  wp-submit
    sleep  3
    input text  user_login  ${USER_NAME}
    input text  user_pass  ${USER_PASSWORD}
    click button  wp-submit