from os import wait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from ..utils import constants
from ..utils.data_processing import convert_tuple_to_dict, is_empty_string
from ..utils.logging_helpers import get_logger
from ..utils.web_scraping import (
    html_input_has_value,
    with_random_delay,
    open_link_in_new_tab,
    wait_elements_until_visible_by_css_selector,
)


def scrape_offices(scraping_config):
    """Returns a list of office objects scraped from the Budget's locations page.
    An office object is composed of a name and address.
    """
    logger = get_logger(__name__)

    headless = scraping_config["headless"]
    wait_element_timeout = scraping_config["wait_element_timeout"]
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(constants.BUDGET_COMPANY_LOCATIONS_PAGE_URL)

    try:
        location_links = wait_elements_until_visible_by_css_selector(
            driver, wait_element_timeout, ".wl-location-state li a"
        )
        __scrape_office_enhanced = with_random_delay(__scrape_office)
        offices = []
        for location_link in location_links:
            office = convert_tuple_to_dict(
                __scrape_office_enhanced(driver, scraping_config, location_link),
                ["name", "address"],
            )
            if not is_empty_string(office["address"]):
                offices.append(office)
            else:
                logger.info(
                    "Office '{}' is excluded because its address is empty.".format(
                        office["name"]
                    )
                )
    finally:
        driver.quit()

    return offices


def __scrape_office(driver, scraping_config, location_link):
    name = location_link.text
    address = ""

    logger = get_logger(__name__)

    current_window_handle = driver.current_window_handle
    open_link_in_new_tab(location_link)
    new_window_handle_index = driver.window_handles.index(current_window_handle) + 1
    new_window_handle = driver.window_handles[new_window_handle_index]
    driver.switch_to.window(new_window_handle)

    wait_element_timeout = scraping_config["wait_element_timeout"]
    try:
        pick_up_location_input = WebDriverWait(driver, wait_element_timeout).until(
            html_input_has_value((By.CSS_SELECTOR, "#PicLoc_value"))
        )
    except:
        logger.exception(f"Can't get the address of the office: {name}")
    else:
        address = pick_up_location_input.get_attribute("value")
    finally:
        driver.close()
        driver.switch_to.window(current_window_handle)

    return (
        name,
        address,
    )
