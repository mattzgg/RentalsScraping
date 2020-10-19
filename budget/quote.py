from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from utils import constants

import time


def scrape_quotes(booking_request):
    pick_up_location_input_value = booking_request["pick_up_location_input_value"]
    drop_off_location_input_value = booking_request["drop_off_location_input_value"]
    pick_up_date = booking_request["pick_up_date"]
    pick_up_time = booking_request["pick_up_time"]
    drop_off_date = booking_request["drop_off_date"]
    drop_off_time = booking_request["drop_off_time"]

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(constants.BUDGET_BOOKING_PAGE_URL)

    fill_pick_up_location(driver, pick_up_location_input_value)

    time.sleep(60)

    driver.quit()


def fill_pick_up_location(driver, input_value):
    # find the pick_up_location input
    try:
        pick_up_location_input = WebDriverWait(
            driver, constants.BUDGET_SCRAPE_QUOTES_TIMEOUT
        ).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#PicLoc_value")))
    except TimeoutException:
        raise RuntimeError("Cannot find pick-up location input on the page.")
    pass

    pick_up_location_input.send_keys(input_value)

    try:
        suggested_pick_up_location_element = WebDriverWait(
            driver, constants.BUDGET_SCRAPE_QUOTES_TIMEOUT
        ).until(presence_of_match_from_suggested_locations(input_value))
    except TimeoutException:
        raise RuntimeError("Cannot find suggested pick-up location on the page.")
    else:
        suggested_pick_up_location_element.click()


class presence_of_match_from_suggested_locations:
    def __init__(self, input_value):
        self.input_value = input_value

    def __call__(self, driver):
        suggested_locations = driver.find_elements(
            By.CSS_SELECTOR, ".angucomplete-description"
        )
        if suggested_locations:
            for suggested_location in suggested_locations:
                print(suggested_location.text)
                if suggested_location.text == self.input_value:
                    return suggested_location
            return False
        else:
            return False