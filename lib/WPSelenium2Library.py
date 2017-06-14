import Selenium2Library
import GeneralLibrary


class WPSelenium2Library(Selenium2Library):


    def set_privacy(self, mode='NA', password='123456'):
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
        self.click_link('//*[@id=\"misc-publishing-actions\"]/div[3]/a')
        hour = time[0,2]
        minute = time[2,4]
        if time[4] == 0:
            day = time[5]
        else:
            day = time[4,6]
        if time[6] == 0:
            month = time[7]
        else:
            month = time[6,8]
        year = time[8:]
        status = GeneralLibrary.check_datetime(day, month, year)
        if status == True:
            self.select_from_list_by_value('mm',month)
            self.input_text('jj',day)
            self.input_text('aa',year)
            if 0<=hour<=23:
                self.input_text('hh',hour)
            if 0<=minute<=59:
                self.input_text('mn',minute)
            self.click_link('//*[@id="timestampdiv"]/p/a[1]')

    def create_post(self, title,content,privacy='NA',password='123456',time='NA'):
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains('Title')
        self.click_link('Add New')
        self.input_text(title,title)
        self.click_button('content-html')
        self.input_text(content,content)
        if privacy != 'NA':
            self.set_privacy(privacy,password)
        if time != 'NA':
            self.publish_time(time)

    def submit_post(self, title):
        self.click_button('publish')
        self.wait_until_page_contains('Edit Post')
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains(title)

    def click_checkbox_post(self, text):
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
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Posts\']')
        self.wait_until_page_contains(text)
        check = self.click_checkbox_post(text)
        if check != 'not':
            self.select_from_list_by_value('bulk-action-selector-top','trash')
            self.click_button('doaction')
            self.wait_until_page_contains('moved to the Trash')


    def choose_file_upload(self,path):
        status = GeneralLibrary.check_filesize(path)
        if status == True:
            self.choose_file('//input[starts-with(@id,\'html5_\')]',path)

    def upload_file(self,path):
        file_name = path[(path.find('/')+1):]
        self.choose_file_upload(path)
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Media\']')
        self.wait_until_page_contains(file_name)

    def upload_folder(self,path):
        list_files = self.list_files_in_directory(path)
        for file in list_files:
            file_path = path + '/' + file
            self.choose_file_upload(file_path)
            self.wait_until_page_contains(file)
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Media\']')

    def upload_media(self,mode,path):
        self.click_element('//*[@class=\'wp-menu-name\'][text()=\'Media\']')
        self.wait_until_page_contains('Media Library')
        self.click_element('//h1[contains(text(),\'Media Library\')]/a')
        mode = mode.lower()
        if mode == 'file':
            self.upload_file(path)
        if mode == 'folder':
            self.upload_folder(path)