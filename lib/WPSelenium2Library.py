import Selenium2Library
import os

class WPSelenium2Library(Selenium2Library):

	def set_privacy(mode='NA',password='123456'):
		mode = mode.lower()
		self.click_link(//*[@id="visibility"]/a)
		if mode == 'private':
			self.select_checkbox(visibility-radio-private)
		elif mode == 'password':
			self.select_checkbox(visibility-radio-password)
			self.input_text(post_password,password)
		else:
			self.select_checkbox(visibility-radio-public)
		self.click_link(//*[@id="post-visibility-select"]/p/a[1])
		
	def check_datetime(day,month,year):
        day = int(day)
		month = int(month)
		year = int(year)
		if month==2:
			if year%4==0:
				if 1<=day<=29:
					return True
				else:
					return False
			else:
				if 1<=day<=28:
					return True
				else:
					return False
		elif month in {1,3,5,7,8,10,12}:
			if 1<=day<=31:
				return True
			else:
				return False
		elif month in {4,6,9,10}:
			if 1<=day<=30:
				return True
			else:
				return False
		else:
			return False

	def publish_time(time):
		self.click_link(//*[@id="misc-publishing-actions"]/div[3]/a)
		hour = time[0,2]
		minute = time[2,4]
		if time[4] == 0:
			day = time[5]
		else:
			day = time[4,6]
		if time[6] == 0:
			month = time[7]
		else
			month = time[6,8]
		year = time[8:]
		status = check_datetime(day,month,year)
		if status == True:
			self.select_from_list_by_value(mm,month)
			self.input_text(jj,day)
			self.input_text(aa,year)
			if 0<=hour<=23:
				self.input_text(hh,hour)
			if 0<=minute<=59:
				self.input_text(mn,minute)
			self.click_link(//*[@id="timestampdiv"]/p/a[1])
	
	def create_post(title,content,privacy='NA',password='123456',publish_time='NA'):
		self.click_element(//*[@class='wp-menu-name'][text()='Posts'])
		self.wait_until_page_contains('Title')
		self.click_link(Add New)
		self.input_text(title,title)
		self.click_button(content-html)
		self.input_text(content,content)
		if privacy != 'NA':
			set_privacy(privacy,password)
		if publish_time != 'NA':
			publish_time(publish_time)
		
	def submit_post(title):
		self.click_button(publish)
		self.wait_until_page_contains('Edit Post')
		self.click_element(//*[@class='wp-menu-name'][text()='Posts'])
		self.wait_until_page_contains(title)
		
#	def click_checknox_post(text):
#		if text == '':
#			self.select_checkbox(cb-select-all-1)
#			return 'ok'
#		list_element = self.get_webelements(//a[contains(text(),'text')]/../../../th/input)

#	def delete_post(text):
#		self.click_element(//*[@class='wp-menu-name'][text()='Posts'])
#		self.wait_until_page_contains(text)
#		check = click_checknox_post(text)
#		if check != 'not':
#			self.select_from_list_by_value(bulk-action-selector-top,'trash')
#			self.click_button(doaction)
#			self.wait_until_page_contains('moved to the Trash')

	def check_filesize(file_path):
		if os.stat(file_path).st_size <= 2**21:
			return True
		else:
			return False
	
	def choose_file_upload(path):
		status = check_filesize(path)
		if status == True:
			self.choose_file(//input[starts-with(@id,'html5_')],path)
			
	def upload_file(path):
		file_name = path[(path.find('/')+1):]
		choose_file_upload(path)
		self.click_element(//*[@class='wp-menu-name'][text()='Media'])
		self.wait_until_page_contains(file_name)
		
	def upload_folder(path):
		list_files = self.list_files_in_directory(path)
		for file in list_files:
			file_path = path + '/' + file
			choose_file_upload(file_path)
			self.wait_until_page_contains(file)
		self.click_element(//*[@class='wp-menu-name'][text()='Media'])
		
	def upload_media(mode,path):
		self.click_element(//*[@class='wp-menu-name'][text()='Media'])
		self-wait_until_page_contains('Media Library')
		self.click_element(//h1[contains(text(),'Media Library')]/a)
		mode = mode.lower()
		if mode == 'file':
			upload_file(path)
		if mode == 'folder':
			upload_folder(path)