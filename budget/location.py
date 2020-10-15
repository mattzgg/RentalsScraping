from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from utils import constants
from utils.datatype import convert_tuple_to_dict
from utils.web_scraping import (
    html_input_has_value,
    with_random_delay,
    open_link_in_new_tab,
)


def scrape_locations():
    """Returns a list of location names scraped from the Budget's location page"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(constants.BUDGET_COMPANY_LOCATIONS_PAGE_URL)

    locations_container_css_selector = ".wl-location-state"

    try:
        locations_container = WebDriverWait(
            driver, constants.BUDGET_SCAPE_LOCATIONS_TIMEOUT
        ).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, locations_container_css_selector)
            )
        )
    except TimeoutException:
        raise RuntimeError("Cannot find locations on the page.")

    location_link_css_selector = locations_container_css_selector + " li a"
    location_links = driver.find_elements_by_css_selector(location_link_css_selector)
    __scrape_location_input_value_enhanced = with_random_delay(
        __scrape_location_input_value
    )
    locations = []
    for location_link in location_links:
        location = convert_tuple_to_dict(
            __scrape_location_input_value_enhanced(driver, location_link),
            ["name", "input_value"],
        )
        locations.append(location)

    driver.quit()

    return locations


def __scrape_location_input_value(driver, location_link):
    location_name = location_link.text
    current_window_handle = driver.current_window_handle

    open_link_in_new_tab(location_link)
    new_window_handle_index = driver.window_handles.index(current_window_handle) + 1
    new_window_handle = driver.window_handles[new_window_handle_index]
    driver.switch_to.window(new_window_handle)

    try:
        pick_up_location_input = WebDriverWait(
            driver, constants.BUDGET_SCAPE_LOCATIONS_TIMEOUT
        ).until(html_input_has_value((By.CSS_SELECTOR, "#PicLoc_value")))
    except TimeoutException:
        raise RuntimeError("Cannot find the pick-up location on the page.")

    location_input_value = pick_up_location_input.get_attribute("value")

    driver.close()
    driver.switch_to.window(current_window_handle)

    return (
        location_name,
        location_input_value,
    )
