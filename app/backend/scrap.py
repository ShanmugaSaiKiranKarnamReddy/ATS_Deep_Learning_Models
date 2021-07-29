from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

skill = input ("Enter skill :") 
DRIVER_PATH = "C:\\Users\\Vicky\\source\\university work\\case-study-1-october2019-case-study-group-2\\my-app\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=' + skill +'&city=&country=&region=&county=&query_options=&')

driver.implicitly_wait(10)



# print(links)
elems = driver.find_elements_by_css_selector(".job-link")
links = [elem.get_attribute('href') for elem in elems]


for link in links:
    print(link)


driver.get('https://www.amazon.jobs/en/search?offset=10&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=' + skill +'&city=&country=&region=&county=&query_options=&')

driver.implicitly_wait(10)



# print(links)
elems = driver.find_elements_by_css_selector(".job-link")
links = [elem.get_attribute('href') for elem in elems]


for link in links:
    print(link)


driver.get('https://www.amazon.jobs/en/search?offset=20&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=' + skill +'&city=&country=&region=&county=&query_options=&')

driver.implicitly_wait(10)



# print(links)
elems = driver.find_elements_by_css_selector(".job-link")
links = [elem.get_attribute('href') for elem in elems]


for link in links:
    print(link)