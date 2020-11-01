from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from utils import constants
from utils.datatype import convert_tuple_to_dict
from utils.web_scraping import (
    html_text_has_been_added,
    with_random_delay,
    open_link_in_new_tab,
    wait_element_until_present_by_xpath,
)


def scrape_locations():
    """Returns a list of location objects scraped from the GO Rentals's locations page.
    A location object composes a name and an address.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(constants.GORENTALS_COMPANY_LOCATIONS_PAGE_URL)

    locations_container_xpath = "/descendant::ul[2]"
    locations_container = wait_element_until_present_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        locations_container_xpath,
    )

    location_link_xpath = locations_container_xpath + "/li//a"
    location_links = driver.find_elements_by_xpath(location_link_xpath)
    __scrape_location_address_enhanced = with_random_delay(__scrape_location_address)
    locations = []
    for location_link in location_links:
        location = convert_tuple_to_dict(
            __scrape_location_address_enhanced(driver, location_link),
            ["name", "address"],
        )
        locations.append(location)

    driver.quit()

    return locations


def __scrape_location_address(driver, location_link):
    location_name = location_link.text
    current_window_handle = driver.current_window_handle

    open_link_in_new_tab(location_link)
    new_window_handle_index = driver.window_handles.index(current_window_handle) + 1
    new_window_handle = driver.window_handles[new_window_handle_index]
    driver.switch_to.window(new_window_handle)

    try:
        # It seems that more time is need to wait for the address to appear.
        location_address_p = WebDriverWait(driver, constants.SCRAPE_TIMEOUT * 3).until(
            html_text_has_been_added((By.XPATH, "/descendant::figure[2]//p[2]"))
        )
    except TimeoutException:
        raise RuntimeError("Cannot find the <p> for the location address on the page.")

    location_address = location_address_p.text

    driver.close()
    driver.switch_to.window(current_window_handle)

    return (
        location_name,
        location_address,
    )
