import time,traceback,builtins,os
from watson import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException


class Error(Exception):
   """Base class for other exceptions"""
   pass

class NoMoreChatsFound(Error):
   """Raised when there are no more chats to traverse"""
   pass

def loop(root):
	i = 0
	while True:
		driver.execute_script('arguments[0].scrollTop=arguments[1]',root,72*i)
		time.sleep(2)
		i+=1

def get_chat(driver,pane,prevChat=None):
	visibleChats = [x for x in driver.find_elements_by_xpath('//div[@id="pane-side"]/div[1]/div/div/div')]
	if visibleChats:
		if prevChat:
			topChat = list(filter(lambda x:x.location['y']>prevChat.location['y'],visibleChats))
		else:
			topChat = visibleChats
		if not topChat:
			raise NoMoreChatsFound('No Unread Chats')
		else:
			topChat = sorted(topChat,key=lambda x:x.location['y'])
		return topChat[0]
	else:
		raise NoMoreChatsFound('No Unread Chats')


def main():
	firefoxProfile = webdriver.FirefoxProfile(os.path.join(os.getcwd(),'firefoxProfile'))
	firefoxProfile.set_preference("browser.sessionstore.restore_on_demand", False)
	firefoxProfile.set_preference('browser.download.dir', os.getcwd())
	message_queue = []
	delay=2
	driver = webdriver.Firefox(firefox_profile=firefoxProfile)
	driver.get('https://web.whatsapp.com')
	# css_soup = BeautifulSoup(driver.get_source)
	# landing = css_soup.find("div", class_="landing-window")
	# if(css_soup.find("div", class_="landing-window") && css_soup.find("div", class_="landing-window"))
	while True:
		try:
			WebDriverWait(driver, delay*5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".app-wrapper-web .app.two")))
			# message += 
			# scroll to bottom of #pane-side
			# new_message_xpath = '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/div/span'
			# new_messages = [x for x in driver.find_elements_by_xpath(new_message_xpath) if x.get_attribute('class') != '']
			# new_messages_class = new_messages[0].get_attribute('class') if len(new_messages) else ''
			# messages = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div/div/div/div/div') #.//div/div/div[2]/div[1]/div[2]
			# messages = sorted([(x,x.location['y']) for x in driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div')],key=lambda x:x[1])
			pane = driver.find_element_by_id('pane-side')
			prevChat = None
			while True:
				try:
					topChat = get_chat(driver,pane,prevChat)
					# process chat
					print(topChat.find_element_by_xpath('.//span[@dir="auto"]').text)
					try:
						numUnread = topChat.find_element_by_xpath('.//div/div/div[2]/div[2]/div[2]/span[1]/div/span').text
						if numUnread != '':
							topChat.click()
							chatBox = driver.find_element_by_id('main')
							messagesUnread = [x.text for x in chatBox.find_elements_by_css_selector('.message-in span.selectable-text[dir=ltr]')][-1*int(numUnread):]
							username = chatBox.find_element_by_css_selector('span[dir=auto]').text
							replies = get_response(username,messagesUnread)
							messageInput = chatBox.find_element_by_xpath('./footer/div[1]/div[2]/div/div[2]')
							for reply in replies:
								messageInput.send_keys(reply)
							else:
								messageInput.send_keys(Keys.RETURN)
					except NoSuchElementException:
						print('\t','No New Message')
					# end processing
					driver.execute_script('arguments[0].scrollTop+=arguments[1]',pane,topChat.size['height'])
					prevChat = topChat
				except StaleElementReferenceException:
					time.sleep(delay/2)
				except NoMoreChatsFound as err:
					print('\t',err,'Going to sleep')
					time.sleep(delay*10)
			break
		except Exception as err:
			print(traceback.format_exc())
			input('Approve Browser login to Whatsapp and Enter any key to continue')


if __name__ == '__main__':
	builtins.sessions = {}
	main()