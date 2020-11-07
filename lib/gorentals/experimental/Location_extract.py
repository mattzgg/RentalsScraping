import time
from selenium import webdriver
import mysql.connector

driver=webdriver.Chrome()
driver.implicitly_wait(8)

# Open GoRentals' location page
driver.get("https://www.gorentals.co.nz/rental-car-locations")

# Get the location names
locations =[]
location_elements = driver.find_elements_by_css_selector('span.marginLeft-6>a')
for element in location_elements:
    result = element.text
    locations.append(result)
print(locations)

# location_addresses =[]
# location_elements = driver.find_elements_by_css_selector(
#     'div > content > div > ul > li > span.marginLeft-6 > a')
# for location_element in location_elements:
#     driver.execute_script("arguments[0].click();",location_element)
#     result = driver.find_element_by_css_selector(
#         'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
#     location_addresses.append(result)
#     element = driver.find_element_by_css_selector('nav >span + a')
#     driver.execute_script("arguments[0].click();", element)
# print(location_addresses)

# Get location addresses
location_addresses = []

# Enter the page of location_1 (Auckland City)
location_elements[0].click()

# Get the address of location_1 (Auckland City)
result = driver.find_element_by_css_selector(
    'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
location_addresses.append(result)

# Go back to the location main page
element = driver.find_element_by_css_selector('nav >span + a')
driver.execute_script("arguments[0].click();",element)


# # Enter the page of location_2 (Auckland Airport)
element = driver.find_element_by_css_selector(
    'div > content > div > ul > li:nth-child(2) > span.marginLeft-6 > a')
driver.execute_script("arguments[0].click();",element)

# Get the address of location_2 (Auckland Airport)
time.sleep(1)
result = driver.find_element_by_css_selector(
    'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
location_addresses.append(result)

# # Go back to the location main page
element = driver.find_element_by_css_selector('nav >span + a')
driver.execute_script("arguments[0].click();",element)

# # Enter the page of location_3 (Wellington Airport)
element = driver.find_element_by_css_selector(
    'div > content > div > ul > li:nth-child(3) > span.marginLeft-6 > a')
driver.execute_script("arguments[0].click();",element)
#
# # Get the address of location_3 (Wellington Airport)
result = driver.find_element_by_css_selector(
    'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
location_addresses.append(result)

# Go back to the location main page
time.sleep(1)
element = driver.find_element_by_css_selector('nav >span + a')
driver.execute_script("arguments[0].click();",element)

# # Enter the page of location_4 (Christchurch Airport)
time.sleep(1)
driver.find_element_by_css_selector(
    'div > content > div > ul > li:nth-child(4) > span.marginLeft-6 > a').click()
#
# # Get the address of location_4 (Christchurch Airport)
time.sleep(1)
result = driver.find_element_by_css_selector(
    'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
location_addresses.append(result)

# # Go back to the location main page
time.sleep(1)
element = driver.find_element_by_css_selector('nav >span + a')
driver.execute_script("arguments[0].click();",element)

# # Enter the page of location_5 (Queenstown Airport)
driver.find_element_by_css_selector(
    'div > content > div > ul > li:nth-child(5) > span.marginLeft-6 > a').click()

# Get the address of location_5 (Queenstown Airport)
time.sleep(1)
result = driver.find_element_by_css_selector(
    'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
location_addresses.append(result)

# # Go back to the location main page
time.sleep(1)
element = driver.find_element_by_css_selector('nav >span + a')
driver.execute_script("arguments[0].click();",element)

# # Enter the page of location_6 (Dunedin Airport)
driver.find_element_by_css_selector(
    'div > ul > li:nth-child(6) > span.marginLeft-6 > a').click()

# # Get the address of location_6 (Dunedin Airport)
time.sleep(1)
result = driver.find_element_by_css_selector(
    'p.fontFamily-bold + p.fontSize-14').get_attribute('textContent')
location_addresses.append(result)
print(location_addresses)

#
# # Create the address_name list
# location_name = [location_name_1,location_name_2,location_name_3,location_name_4,
#                  location_name_5,location_name_6]
# print(location_name)
#
# # Create the address_address list
# location_address = [location_address_1,location_address_2,location_address_3,
#                     location_address_4,location_address_5,location_address_6]
# print(location_address)
#
# # Create GoRentals' company_id list whose number of value can be identical to the number of locations
# company_id = 3
# company_ids =[ ]
# a = 1
# b =len(location_name) + 1
# while a < b:
#         company_ids.append(company_id)
#         a += 1
#         if a == b:
#             break
#
# # Wait 5 second before quiting the browser
# time.sleep(5)
#
# # Quit the browser
# driver.quit()
#
# # Connect to the project database
# mydb = mysql.connector.connect(
#     host = "ucmysqlacis01p.linux.canterbury.ac.nz",
#     port =  3306,
#     database ="MBIS680_rentals_prices",
#     user = "zwa91",
#     password = "Wz59124808_"
# )
# print(mydb)
#
# # Define the Cursor
# my_cursor = mydb.cursor()
#
# # Select the Database
# my_cursor.execute('USE MBIS680_rentals_prices')
#
# # Insert address_name into the address table
# # my_cursor.execute('INSERT INTO location(id) VALUE (1)')
# my_cursor.executemany("INSERT INTO location(name,company_id) VALUES (%s,%s)", location_name,company_ids)
#
