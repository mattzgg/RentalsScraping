import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lib.utils.constants import *
from lib.utils.web_scraping import *

driver=webdriver.Chrome()
driver.implicitly_wait(8)
# Open the Gorentals' main page
driver.get(constants.GORENTALS_COMPANY_MAIN_PAGE_URL)

driver.find_element_by_id('locationPickerStart').click()
elements = driver.find_elements_by_css_selector('div.multiselect__tags > span.multiselect__single')
for element in elements:
    print(element.text)
