import Selenium2Library

class WPSelenium2Library(Selenium2Library):

	def set_privacy(mode='NA',password='123456'):
		mode = mode.lower()
		self.click_link(//*[@id="visibility"]/a)