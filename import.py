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
driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
print('loading page')
driver.get ('https://learn.homeschoolacademy.com/index.cfm')
driver.execute_script("changeTab('L')")
driver.find_element_by_id('txtusername').send_keys(os.environ.get('BRIDGEWAY_USERNAME'))
driver.find_element_by_id ('txtpassword').send_keys(os.environ.get('BRIDGEWAY_PASSWORD'))
elem = driver.find_element_by_name('txtpassword')
print('logging in')
elem.send_keys(Keys.RETURN)
#driver.execute_script('chkLogin()')
print('getting redirect')
corner_boxes = driver.find_elements_by_class_name('cornerBox')
for corner_box in corner_boxes:
    onclick = corner_box.get_attribute('onclick')
    if onclick and onclick.startswith("javascript:location.href='index.cfm/pg/MySchool/s/mycourses"):
        match = re.search(r'location.href=[\'"]?([^\'" >]+)', onclick)
        url = match.group(1)
        print('Found courses link . . . navigating to https://{}'.format(url))
        driver.get('https://learn.homeschoolacademy.com/{}'.format(url))
        break
urls = []
view_progress_links = driver.find_elements_by_link_text('view progress')

for link in view_progress_links:
    urls.append(link.get_attribute('href'))
data = {}
for url in urls:
    subject_row = None
    subject = None
    print('Going to View Progress page: {}'.format(url))
    driver.get(url)
    print('sleeping for 5')
    time.sleep(5)
    table = driver.find_element_by_class_name("black")
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        if 'navajowhite' in row.get_attribute("style"):
            subject_row = row
            break
    if not subject_row:
        print("No selected subject found")
        continue
    i = 0
    for c in subject_row.find_elements_by_tag_name("td"):
        print('{}:{}'.format(i, c.text))
        if i == 0:
            subject = c.text
            print('Getting data for {}'.format(subject))
            data[subject] = {}
            data[subject]['assignments'] = {}
        if i == 3:
            data[subject]['percentage'] = c.text
        if i == 4:
            data[subject]['grade'] = c.text
        i = i + 1
    try:
        assignment_table = table.find_element_by_tag_name("table")
    except NoSuchElementException:
        print('No activities for this class')
        continue
    assignment_re = re.compile("[0-9]+\.[0-9]+")
    rows = assignment_table.find_elements_by_tag_name("tr")
    for row in rows:
        date = ""
        cols = row.find_elements_by_tag_name("td")
        i = 0
        for c in cols:
            if i == 0:
                assignment = c.text.strip()
            if i == 2:
                date = c.text.strip()
                if not date:
                    date = "X"
            i = i + 1
            data[subject]['assignments'][assignment] = date
    pp = pprint.PrettyPrinter()
    pp.pprint(data[subject])
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
