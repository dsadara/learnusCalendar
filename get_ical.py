import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import getpass


# enter Learnus ID PW
id = input('Enter the ID : ')
pw = getpass.getpass('Enter the PW : ')

# webdriver setting
options = webdriver.ChromeOptions()
options.add_argument('headless')
s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)

# go to Learnus page
driver.get('https://www.learnus.org/login.php')

time.sleep(1)

# enter id pw by webdriver
e = driver.find_elements(By.CLASS_NAME, 'form-control')[1]
e.send_keys(id)

e = driver.find_elements(By.CLASS_NAME, 'form-control')[2]
e.send_keys(pw)
e.send_keys(Keys.ENTER)

time.sleep(2)

# go to calendar page in Learnus
driver.get('https://www.learnus.org/calendar/view.php?view=month')

e = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-secondary')))[1]
e.click()

time.sleep(1)

# check import options
e = driver.find_elements(By.ID, 'id_events_exportevents_all')[0]
e.click()

e = driver.find_elements(By.ID, 'id_period_timeperiod_monthnow')[0]
e.click()

e = driver.find_elements(By.ID, 'id_generateurl')[0]
e.click()


# get .ical file download URL
e = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'calendarurl')))[0]
urlWithString = e.text

# url triming
downloadURL = urlWithString.split()[3]
print(downloadURL)

# download to current directory
r = requests.get(downloadURL, allow_redirects=True)
open('icalexport.ics', 'wb').write(r.content)