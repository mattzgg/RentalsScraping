
# Open Gorentals location webpage

GORENTALS_COMPANY_MAIN_PAGE_URL = "https://www.gorentals.co.nz/"
car_models = []
car_features_elements = [
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(1) > div > div:nth-child(1) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(2) > div > div:nth-child(2) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(1) > div > div:nth-child(3) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(1) > div > div:nth-child(4) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(1) > div > div:nth-child(5) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(2) > div > div:nth-child(1) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(2) > div > div:nth-child(2) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(2) > div > div:nth-child(3) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(2) > div > div:nth-child(4) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(3) > div > div:nth-child(1) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(3) > div > div:nth-child(2) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(3) > div > div:nth-child(3) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(3) > div > div:nth-child(4) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(4) > div > div:nth-child(1) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(4) > div > div:nth-child(2) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(4) > div > div:nth-child(3) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(4) > div > div:nth-child(4) > article > footer > p > button > span',
'#__layout > div > div.flex-1-0-auto > main > content > section > content > div:nth-child(5) > div > div > article > footer > p > button > span'
]
def get_car_model_name ():
    import time
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("https://www.gorentals.co.nz/vehicles/")
    time.sleep(2)
    global car_models
    for car_model_name in driver.find_elements_by_css_selector('[class="fontSize-16 fontFamily-bold whiteSpace-nowrap backgroundImage-goGradientElipsis"'):
        result = car_model_name.text
        car_models.append(result)
        # print(result)
    print(f'Hello! There are {len(car_models)} car_models in GoRentals.')
    print(car_models)
    driver.close()

# Get car features
def get_feature(car_features_element):
    import time
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("https://www.gorentals.co.nz/vehicles/")
    global car_features_elements
    car_feature_list_temp =[]
    # Get car features for car 1
    driver.find_element_by_css_selector(car_features_element).click()
    time.sleep(2)
    for car_feature in driver.find_elements_by_tag_name('li'):
        result = car_feature.text
        car_feature_list_temp.append(result)
    car_feature_list = car_feature_list_temp[-13:-1]
    print(car_feature_list)
    driver.close()
def get_car_feature ():
    for car_features_element in car_features_elements:
        get_feature(car_features_element)

# def list_locators ():
#     from selenium import webdriver
#     import time
#     driver = webdriver.Chrome()
#     driver.get("https://www.gorentals.co.nz/vehicles/")
#     elements = driver.find_elements_by_css_selector('#__layout > div > div.flex-1-0-auto > main > content > section > content > div > div > div > article > footer > p > button > span')
#     element_1 = elements[0]
#     print(element_1)
#     element_1.click()
    # for element in elements:
    #     driver.get("https://www.gorentals.co.nz/vehicles/")
    #     # js = 'window.open("https://www.gorentals.co.nz/vehicles/");'
    #     # driver.execute_script(js)
    #     element.click()
    #     car_feature_list_temp = []
    #     # Get car features for car 1
    #     time.sleep(2)
    #     for car_feature in driver.find_elements_by_tag_name('li'):
    #         result = car_feature.text
    #         car_feature_list_temp.append(result)
    #     car_feature_list = car_feature_list_temp[-13:-1]
    #     print(car_feature_list)
    #     driver.close()

# list_locators()
