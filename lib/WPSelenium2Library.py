import Selenium2Library

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
		
		