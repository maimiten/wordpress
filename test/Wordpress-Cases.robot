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
@{USERLIST}  tthomas  harveyjenna  uhall


*** Test Cases ***

Create New Post
    [Tags]  1
    Log In
#    Create Text Post  First Post  This a test
#    Create Text Post  Private post  Only me can see this  privacy=private
#    Create Video Post  Helsinki Air Show 2017  https://www.youtube.com/watch?v=RaaSHDbdJPk
#    Create Video Post  Kem's Samba dance  https://www.youtube.com/watch?v=gfT4Sk-4QMk  privacy=password
    Create post from file  Short blog  C:/git-course/wordpress/data/content.txt  time=220515062017

Upload New Media
    [Tags]  2
    Log In
    Upload media  file  C:/git-course/wordpress/data/Desert.jpg
    Upload media  folder  C:/git-course/wordpress/data/flower

Add New User
    [Tags]  3
    Log In
    Add User  datalist=@{DATALIST1}  noti=no  role=edit

Delete User
    [Tags]  4
    Log In
    Delete User  userlist=@{USERLIST}

Change User Role
    [Tags]  5
    Log In
    Change Role  userlist=@{USERLIST}  role=Editor

User Flow
    [Tags]  6
    Log In  ${USER_NAME}  ${USER_PASSWORD}
    &{USERDATA} =  Add User  datalist=@{DATALIST1}  role=ctrb
    Log Out
    Log In  &{USERDATA}[username]  &{USERDATA}[password]





