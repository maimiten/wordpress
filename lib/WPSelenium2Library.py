from Selenium2Library import Selenium2Library
import GeneralLibrary
from faker import Faker
from robot.api import logger


class WPSelenium2Library(Selenium2Library):

    def set_privacy(self, mode='NA', password='123456'):
        '''
        This keyword set the privacy for the post with the provided *mode* and *password*.
        Both *mode* and *password* are optional. If *password* is not provided, then default password wiil be used.
        '''
        mode = mode.lower()
        self.click_link('//*[@id="visibility"]/a')
        if mode == 'private':
            self.select_checkbox('visibility-radio-private')
        elif mode == 'password':
            self.select_checkbox('visibility-radio-password')
            self.input_text('post_password', password)
        else:
            self.select_checkbox('visibility-radio-public')
            self.click_link('//*[@id="post-visibility-select"]/p/a[1]')


    def publish_time(self, time):
        '''
        This keyword will set the _time_ which is provided by user to publish the post.
        '''
        self.click_link('//*[@id=\"misc-publishing-actions\"]/div[3]/a')
        hour = time[0:2]
        minute = time[2:4]
        if time[4] == 0:
            day = time[5]
        else:
            day = time[4:6]
        if time[6] == 0:
            month = time[7]
        else:
            month = time[6:8]
        year = time[8:]
        status = GeneralLibrary.check_datetime(day, month, year)
        if status == True:
            self.select_from_list_by_value('mm',month)
            self.input_text('jj',day)
            self.input_text('aa',year)
            if 0<=int(hour)<=23:
                self.input_text('hh',hour)
            if 0<=int(minute)<=59:
                self.input_text('mn',minute)
            self.click_link('//*[@id="timestampdiv"]/p/a[1]')

    def create_post(self, title,content,privacy='NA',password='123456',time='NA'):
        '''
        This keyword is used to create a new post with the provided _title_ and _content_.
        _privacy, password_ and _time_ are optional. If these parameter are not provided, the new post is public and will be published after submitting.
        '''
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains('Title')
        self.click_link('Add New')
        self.input_text('title',title)
        self.click_button('content-html')
        self.input_text('content',content)
        if privacy != 'NA':
            self.set_privacy(privacy,password)
        if time != 'NA':
            self.publish_time(time)

    def submit_post(self, title):
        '''
        This keyword will submit the post that is composed in the <a href="file:///C:/git-course/wordpress/docs/WPSelenium2Library.html#Create%20Post">Create Post</a> keyword
        '''
        self.click_button('publish')
        self.wait_until_page_contains('Edit Post')
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains(title)

    def click_checkbox_post(self, text):
        '''
        This keyword selects the post with the _text_ that is provided by user
        '''
        if text == 'NA':
            self.select_checkbox('cb-select-all-1')
            return 'ok'
        locator = '//a[contains(text(),\'' + text + '\')]/../../../th/input'
        list_element = self.get_webelements(locator)
        if list_element == []:
            print 'Sorry, no post found with ', text
            return 'not'
        for element in list_element:
            self.click_element(element)
            return 'ok'

    def delete_post(self,text):
        '''
        This keyword deletes the post with the title includes _text_ provided
        '''
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains(text)
        check = self.click_checkbox_post(text)
        if check != 'not':
            self.select_from_list_by_value('bulk-action-selector-top','trash')
            self.click_button('doaction')
            self.wait_until_page_contains('moved to the Trash')


    def choose_file_upload(self,path):
        '''
        This keyword chooses the file or folder with _path_ provided to upload
        '''
        status = GeneralLibrary.check_filesize(path)
        if status == True:
            self.choose_file('//input[starts-with(@id,\'html5_\')]',path)

    def upload_file(self,path):
        '''
        This keyword will upload the file that has _path_
        '''
        file_name = path[(path.rfind('/')+1):]
        self.choose_file_upload(path)
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Media\']')
        self.wait_until_page_contains(file_name)

    def upload_folder(self,path):
        '''
        This keyword will upload the folder that has _path_
        '''
        list_files = self.list_files_in_directory(path)
        for file in list_files:
            file_path = path + '/' + file
            self.choose_file_upload(file_path)
            self.wait_until_page_contains(file)
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Media\']')

    def upload_media(self,mode,path):
        '''
        This keyword uploads the file or folder that has _path_
        '''
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Media\']')
        self.wait_until_page_contains('Media Library')
        self.click_element('//h1[contains(text(),\'Media Library\')]/a')
        mode = mode.lower()
        if mode == 'file':
            self.upload_file(path)
        if mode == 'folder':
            self.upload_folder(path)

    def create_text_post(self,title,content,privacy='NA',password='123456',time='NA'):
        '''
        This keyword will create a text post with _title_ and _content_ provided
        '''
        self.create_post(title,content,privacy,password,time)
        self.submit_post(title)

    def create_video_post(self,title,content,privacy='NA',password='123456',time='NA'):
        '''
        This keyword will create a post that includes video with _title_ and _content_ provided
        '''
        self.create_post(title,content,privacy,password,time)
        self.select_checkbox('post-format-video')
        self.submit_post(title)

    def create_post_from_file(self,title,filename,privacy='NA',password='123456',time='NA'):
        '''
        This keyword will create a post with _title_ and content is read from the file with _filename_
        '''
        content = GeneralLibrary.read_file(filename)
        self.create_post(title, content, privacy, password, time)
        self.submit_post(title)

    def create_post_and_upload_media(self,title,content,path,privacy='NA',password='123456',time='NA'):
        '''
        This keyword create a post with _title_ and _content_. This post also includes media file with _path_ upload from computer
        '''
        self.create_post(title, content, privacy, password, time)
        self.click_button('insert-media-button')
        self.click_element('//a[text()=\'Upload Files\']')
        self.choose_file_upload(path)
        self.click_button('Insert into post')
        self.submit_post(title)

    def create_post_and_add_media_from_library(self,title,content,filename,privacy='NA',password='123456',time='NA'):
        '''
        This keyword create a post with _title_ and _content_. This post includes media file with _filename_ which is added from wordpress library
        '''
        self.create_post(title, content, privacy, password, time)
        self.click_button('insert-media-button')
        self.click_element('//a[text()=\'Media Library\']')
        locator = '//img[contains(@src,\'' + filename + '\')]/../..'
        self.click_element(locator)
        self.click_button('Insert into post')
        self.submit_post(title)

    def insert_media_from_url(self,url,caption='NA',alt_text='NA'):
        '''
        This keyword is used to *insert* new _media_ into library from a url.
        '''
        self.click_button('insert-media-button')
        self.click_element('//a[text()=\'Insert from URL\']')
        self.clear_element_text('embed-url-field')
        self.input_text('embed-url-field',url)
        if caption != 'NA':
            self.input_text('//textarea[@data-setting=\'caption\']',caption)
        if alt_text != 'NA':
            self.input_text('//input[@data-setting=\'alt\']',alt_text)
        self.click_button('Insert into post')

    def add_category(self,name,slug='NA',description='NA'):
        '''
        This keyword addes new category
        '''
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains('Title')
        self.click_link('Categories')
        self.input_text('tag-name',name)
        if slug != 'NA':
            self.input_text('tag-slug',slug)
        if description != 'NA':
            self.input_text('tag-description',description)
        self.click_button('submit')

    def generate_password(self,password):
        self.click_button('Show password')
        self.clear_element_text('pass1-text')
        self.input_text('pass1-text',password)
        if self.get_text('pass-strength-result') in {'Very weak','Weak'}:
            self.select_checkbox('pw_weak')

    def submit_user(self,username):
        self.click_button('createusersub')
        self.wait_until_page_contains(username)

    def fill_data(self,userdata):
        for key, value in userdata.iteritems():
            if key == 'username':
                self.input_text('user_login',value)
            elif key == 'email':
                self.input_text('email',value)
            elif key == 'firstname':
                self.input_text('first_name',value)
            elif key == 'lastname':
                self.input_text('last_name',value)
            elif key == 'website':
                self.input_text('url',value)
            elif key == 'role':
                if value == 'admin':
                    self.select_from_list_by_value('role', 'administrator')
                elif value == 'edit':
                    self.select_from_list_by_value('role', 'editor')
                elif value == 'ctrb':
                    self.select_from_list_by_value('role', 'contributor')
                elif value == 'au':
                    self.select_from_list_by_value('role', 'author')
                else:
                    self.select_from_list_by_value('role', 'subscriber')


    def generate_userdata(self,datalist,role):
        fake = Faker()
        fakeProfile = fake.profile()
        userdata = {'role':'sub'}
        for i in datalist:
            if i == 'username':
                userdata['username'] = fakeProfile['username']
            elif i == 'email':
                userdata['email'] = fakeProfile['mail']
            elif i == 'firstname':
                userdata['firstname'] = fakeProfile['name'].split()[0]
            elif i == 'lastname':
                userdata['lastname'] = fakeProfile['name'].split()[1]
            elif i == 'password':
                fakepass = fake.password()
                userdata['password'] = fakepass
            elif i == 'website':
                userdata['website'] = fakeProfile['website'][0]
        if role != 'sub':
            userdata['role'] = role
        return userdata

    def add_user(self,datalist,noti='yes',role='sub'):
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Users\']')
        self.wait_until_page_contains('Users')
        self.click_element('//*[@id="menu-users"]//a[text()=\'Add New\']')
        self.wait_until_page_contains('Add New User')
        userdata = self.generate_userdata(datalist,role)
        if 'username' and 'email' in userdata:
            self.fill_data(userdata)
        if 'password' in userdata:
            self.generate_password(userdata['password'])
        if noti == 'no':
            self.unselect_checkbox('send_user_notification')
        self.submit_user(userdata['username'])

    def click_checkbox_user(self,username):
        locator = '//a[text()=\'' + username + '\']/../../../th/input'''
        self.select_checkbox(locator)

    def delete_user(self,userlist):
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Users\']')
        self.wait_until_page_contains('Users')
        for i in userlist:
            self.click_checkbox_user(i)
        self.select_from_list_by_value('bulk-action-selector-top','delete')
        self.click_button('doaction')
        self.wait_until_page_contains('Delete Users')
        self.click_button('submit')
        self.wait_until_page_contains('deleted')

    def change_role(self,userlist,role):
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Users\']')
        self.wait_until_page_contains('Users')
        for i in userlist:
            self.click_checkbox_user(i)
        self.select_from_list_by_value('new_role',role.lower())
        self.click_button('changeit')
        self.wait_until_page_contains('Changed roles')

    def edit_user(self,username):
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Users\']')
        self.wait_until_page_contains('Users')
        self.click_link(username)






