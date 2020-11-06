import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lib.utils import constants
from lib.utils.web_scraping import (
    wait_element_until_visible_by_id,
    wait_element_until_visible_by_xpath,
    wait_element_until_present_by_xpath,
)


def scrape_quotes(non_fulfilled_booking_request):
    pick_up_office_name = non_fulfilled_booking_request["pick_up_office_name"]
    pick_up_office_address = non_fulfilled_booking_request["pick_up_office_address"]
    drop_off_office_name = non_fulfilled_booking_request["drop_off_office_name"]
    drop_off_office_address = non_fulfilled_booking_request["drop_off_office_address"]
    pick_up_date_value = non_fulfilled_booking_request[
        "pick_up_date_value"
    ]  # 06/11/2020
    pick_up_time_value = non_fulfilled_booking_request["pick_up_time_value"]  # 09:00 AM
    drop_off_date_value = non_fulfilled_booking_request["drop_off_date_value"]
    drop_off_time_value = non_fulfilled_booking_request["drop_off_time_value"]

    chrome_options = Options()
    if constants.IS_CHROME_HEADLESS_ENABLED:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(constants.GORENTALS_COMPANY_MAIN_PAGE_URL)

    __fill_location_input(driver, "locationPickerStart", pick_up_office_name)
    __fill_location_input(driver, "locationPickerEnd", drop_off_office_name)
    # pick_up_location_option.click()
    # pick_up_location_select = Select(pick_up_location_input)
    # pick_up_location_select.select_by_visible_text(pick_up_office_name)
    # ----end----

    # Click the drop-off button and select one drop_off_location in the dropbox
    driver.find_element_by_id("locationPickerEnd").click()
    drop_off_location = Select(driver.find_element_by_id("locationPickerEnd"))
    drop_off_location.select_by_visible_text("Christchurch Airport")

    # select one pick_up_date in the calendar
    driver.find_element_by_id("datePickerStart").click()
    element1 = driver.find_element_by_css_selector(
        "#__layout > div > div.flex-1-0-auto > main > header > content > div.position-absolute.top.left.width-span12.height-span12.tablet\:paddingRight-48.desktop\:paddingRight-56 > div > div.flex-1.display-flex.flexDirection-column.justifyContent-flexEnd.paddingTop-16.paddingBottom-16.tablet\:justifyContent-center.tablet\:paddingBottom-8.tabletWide\:paddingBottom-32 > div > div > form > div:nth-child(1) > p.gridColumn-span7 > span > div > div > div.c-header > div:nth-child(3) > svg > path"
    )
    webdriver.ActionChains(driver).move_to_element(element1).click(element1).perform()
    time.sleep(2)
    webdriver.Chrome().refresh
    driver.find_element_by_css_selector(
        "#__layout > div > div.flex-1-0-auto > main > header > content > div.position-absolute.top.left.width-span12.height-span12.tablet\:paddingRight-48.desktop\:paddingRight-56 > div > div.flex-1.display-flex.flexDirection-column.justifyContent-flexEnd.paddingTop-16.paddingBottom-16.tablet\:justifyContent-center.tablet\:paddingBottom-8.tabletWide\:paddingBottom-32 > div > div > form > div:nth-child(1) > p.gridColumn-span7 > span > div > div > div.c-weeks > div > div > div:nth-child(2) > div:nth-child(4) > div > div.c-day-content-wrapper > div > div"
    ).click()

    # Select one pick_up_time in the time dropbox
    driver.find_element_by_id("timePickerStart").send_keys("01:00 PM")

    # select one drop_off_date in the calendar
    driver.find_element_by_id("datePickerEnd").click()
    # element2 = driver.find_element_by_css_selector('#__layout > div > div.flex-1-0-auto > main > header > content > div.position-absolute.top.left.width-span12.height-span12.tablet\:paddingRight-48.desktop\:paddingRight-56 > div > div.flex-1.display-flex.flexDirection-column.justifyContent-flexEnd.paddingTop-16.paddingBottom-16.tablet\:justifyContent-center.tablet\:paddingBottom-8.tabletWide\:paddingBottom-32 > div > div > form > div:nth-child(1) > p.gridColumn-span7 > span > div > div > div.c-header > div:nth-child(3) > svg')
    # webdriver.ActionChains(driver).move_to_element(element2).click(element2).perform()
    time.sleep(2)
    webdriver.Chrome().refresh
    driver.find_element_by_css_selector(
        "#__layout > div > div.flex-1-0-auto > main > header > content > div.position-absolute.top.left.width-span12.height-span12.tablet\:paddingRight-48.desktop\:paddingRight-56 > div > div.flex-1.display-flex.flexDirection-column.justifyContent-flexEnd.paddingTop-16.paddingBottom-16.tablet\:justifyContent-center.tablet\:paddingBottom-8.tabletWide\:paddingBottom-32 > div > div > form > div.tabletWide\:display-grid.gridColumn-span12.tabletWide\:gridColumn-span4.display-grid.gridTemplateColumns-12fr.gridGap-8.marginTop-8.marginBottom-8.tabletWide\:margin-0.display-grid > p.gridColumn-span7 > span > div > div > div.c-weeks > div > div > div:nth-child(3) > div:nth-child(2) > div > div.c-day-content-wrapper > div > div"
    ).click()

    # select one drop_off_date in the calendar
    driver.find_element_by_id("timePickerEnd").send_keys("03:30 PM")

    # Click the "Find my car" button
    driver.find_element_by_css_selector("form > div >button").click()

    # Let the browser wait 2 seconds for opening the price quote page
    time.sleep(2)

    # Get car_category names
    car_categories = []
    elements = driver.find_elements_by_css_selector("content > div > h2")
    for element in elements:
        result = element.text
        car_categories.append(result)
    print(car_categories)

    # Get car_model names
    car_models = []
    time.sleep(1)

    for car_model_name in driver.find_elements_by_css_selector(
        '[class="fontSize-16 fontFamily-bold whiteSpace-nowrap backgroundImage-goGradientElipsis"'
    ):
        result = car_model_name.text
        car_models.append(result)
        # print(result)
    print(car_models)

    # Get car years
    car_years_list = []
    for car_years in driver.find_elements_by_css_selector(
        '[class="fontSize-14 color-goGrayDark"'
    ):
        result = car_years.text
        # print(result)
        car_years_list.append(result)
    print(car_years_list)

    # Get total price
    total_price_list = []
    for total_price in driver.find_elements_by_css_selector(
        '[class="display-inlineBlock lineHeight-20"'
    ):
        result = total_price.text
        total_price_list.append(result)
    print(total_price_list)

    # Get car availability status
    status_list = []
    for status in driver.find_elements_by_css_selector(
        '[class="paddingLeft-8 paddingRight-8"'
    ):
        result = status.text
        status_list.append(result)
    print(status_list)

    time.sleep(2)

    driver.quit()


def __fill_location_input(driver, location_input_id, office_name):
    location_option_xpath = (
        "//label[@for='{}']//ul/li//span[normalize-space(text())='{}']".format(
            location_input_id, office_name
        )
    )
    location_option = wait_element_until_present_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        location_option_xpath,
    )

    location_select_caret_xpath = "//label[@for='{}']//div[@class='{}']".format(
        location_input_id, "multiselect__select"
    )
    location_select_caret = wait_element_until_present_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        location_select_caret_xpath,
    )

    # location_select_caret.click() has problem so use javascript code instead
    driver.execute_script("arguments[0].click();", location_select_caret)
    driver.execute_script("arguments[0].click();", location_option)
