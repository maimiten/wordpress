*** Settings ***
Library  ${CURDIR}/../lib/GeneralLibrary.py
Library  ${CURDIR}/../lib/WPSelenium2Library.py
Resource  Variables.robot
Resource  Keywords.robot
Suite Setup  Begin Web Case
Suite Teardown  End Web Case

*** Variables ***
@{DATALIST1}  username  email  firstname  lastname
@{DATALIST2}  username  email  password  website
&{DATA_CHANGE}  firstname=Mark  visual=yes  color=ocean  toolbar=no  display=lastname

*** Test Cases ***

KemKool web
    [Tags]  kk
    Log In  ${KK_USERNAME}  ${KK_PASSWORD}  ${KK_URL}
    Create Video Post  ${KK_TITLE}  ${KK_CONTENT}  time=${TIME}

Create New Post
    [Tags]  1
    Log In  ${USER_NAME}  ${USER_PASSWORD}

Upload New Media
    [Tags]  2
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    Upload media  file  C:/git-course/wordpress/data/Desert.jpg
    Upload media  folder  C:/git-course/wordpress/data/flower

Add New User
    [Tags]  3
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    Add User  datalist=@{DATALIST1}  noti=no  role=edit

Delete User
    [Tags]  4
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    Delete User  bmontoya

Change User Role
    [Tags]  4
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    Change Role  hendersonscott  Editor

User Flow
    [Tags]  6
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    &{USERDATA} =  Add User  datalist=@{DATALIST1}  role=edit
    Log Out
    Log In  &{USERDATA}[username]  &{USERDATA}[password]
    Edit User  ${USERDATA}  ${DATA_CHANGE}
    Log Out
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    Delete User  &{USERDATA}[username]





