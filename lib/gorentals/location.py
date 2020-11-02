from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from ..utils import constants
from ..utils.datatype import convert_tuple_to_dict
from ..utils.web_scraping import (
    html_text_has_been_added,
    with_random_delay,
    open_link_in_new_tab,
    wait_elements_until_visible_by_xpath,
)


def scrape_offices():
    """Returns a list of office objects scraped from the GO Rentals's locations page.
    An office object is composed of a name and address.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(constants.GORENTALS_COMPANY_LOCATIONS_PAGE_URL)

    location_links = wait_elements_until_visible_by_xpath(
        driver, constants.SCRAPE_TIMEOUT, "/descendant::ul[2]/li//a"
    )
    __scrape_office_enhanced = with_random_delay(__scrape_office)
    offices = []
    for location_link in location_links:
        office = convert_tuple_to_dict(
            __scrape_office_enhanced(driver, location_link),
            ["name", "address"],
        )
        offices.append(office)

    driver.quit()

    return offices


def __scrape_office(driver, location_link):
    name = location_link.text
    current_window_handle = driver.current_window_handle

    open_link_in_new_tab(location_link)
    new_window_handle_index = driver.window_handles.index(current_window_handle) + 1
    new_window_handle = driver.window_handles[new_window_handle_index]
    driver.switch_to.window(new_window_handle)

    try:
        # It seems that more time is need to wait for the address to appear.
        office_address_p = WebDriverWait(driver, constants.SCRAPE_TIMEOUT * 6).until(
            html_text_has_been_added((By.XPATH, "/descendant::figure[2]//p[2]"))
        )
    except TimeoutException:
        raise RuntimeError("Cannot find the <p> for the office address on the page.")

    address = office_address_p.text

    driver.close()
    driver.switch_to.window(current_window_handle)

    return (
        name,
        address,
    )
