#Import libraries
import re
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Login details
login = "Enter email"
password = "enter password"

#start browser session
#driver = webdriver.Chrome(ChromeDriverManager().install())
#os.environ["webdriver.chrome.driver"] = chromedriver
chromedriver = "C:\\Users\\frank\\.anaconda\\navigator\\scripts\\chromedriver.exe"
prefs = {'download.default_directory' : 'D:\Case Study\LinkedIn\javaDeveloper'}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()

#open linkedin in automated browser
driver.get("https://www.linkedin.com/login")
driver.implicitly_wait(10)


#Login
driver.find_element_by_id("username").send_keys(str(login))
password = driver.find_element_by_id("password").send_keys(str(password))
driver.find_element_by_class_name("login__form_action_container").click()
#time.sleep(50)

# Opening Google
driver.get("https://www.google.com")



#Profiles to fetceh cv for 
profiles =['tableau developer']
#,'','','sql developer'

data = []
linkedin_urls = []
for profile in profiles:
        # send_keys() to simulate the search text key strokes
        driver.get("https://www.google.com")
        search_query = driver.find_element_by_name('q')
        search_query.send_keys('site:linkedin.com/in/ and'+str(profile))
        search_query.send_keys(Keys.RETURN)
        time.sleep(6)
        
        #First page
        links = driver.find_elements_by_partial_link_text('a')
        for link in links:
            data.append(link.get_attribute("href"))
        

        #Fetching links of the search results
        for i in range(2,12):
            links = driver.find_elements_by_partial_link_text('a')
            for link in links:
                data.append(link.get_attribute("href"))

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elem = driver.find_element_by_link_text(str(i))
            elem.click()
            time.sleep(5)
            
            
#Removing none,and unrelated links
new = filter(None, data)
for line in new:
    if ".linkedin.com" in line:
        linkedin_urls.append(line)
        driver.implicitly_wait(0.5)

# For loop to iterate over each URL in the list
for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    #click the "more" button
    try: 
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//span[contains(text(),'More')]").click()
        driver.implicitly_wait(10)
    except NoSuchElementException:
        driver.find_element_by_xpath("//button[@id='ember121']//span[contains(text(),'More')]").click()
   
    #Save as pdf option
    while True:
        try:
            li = driver.find_elements_by_class_name("pv-s-profile-actions__overflow-icon")
            li[1].click()
            time.sleep(10)
            break
        except NoSuchElementException:
            print("Couldn't download file")
