import re
import time
import pprint
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
print('loading page')
driver.get ('https://bridgewayacad.rosettastoneclassroom.com/en-US')
driver.find_element_by_id('login_user_user_name').send_keys(os.environ.get('ROSETTA_USERNAME'))
driver.find_element_by_id ('login_user_password').send_keys(os.environ.get('ROSETTA_PASSWORD'))
elem = driver.find_element_by_id('login_user_password')
print('logging in')
elem.send_keys(Keys.RETURN)
reports_url = driver.find_element_by_link_text('My Reports')
print('Opening reports page')
driver.get(reports_url.get_attribute('href'))
