from logging import getLogger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from ..utils import constants
from ..utils.datatype import convert_tuple_to_dict
from ..utils.logging_helpers import get_logger
from ..utils.web_scraping import (
    html_text_has_been_added,
    with_random_delay,
    open_link_in_new_tab,
    wait_elements_until_visible_by_xpath,
)


def scrape_offices(scraping_config):
    """Returns a list of office objects scraped from the GO Rentals's locations page.
    An office object is composed of a name and address.
    """
    headless = scraping_config["headless"]
    wait_element_timeout = scraping_config["wait_element_timeout"]
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(constants.GORENTALS_COMPANY_LOCATIONS_PAGE_URL)
    try:
        location_links = wait_elements_until_visible_by_xpath(
            driver, wait_element_timeout, "/descendant::ul[2]/li//a"
        )
        __scrape_office_enhanced = with_random_delay(__scrape_office)
        offices = []
        for location_link in location_links:
            office = convert_tuple_to_dict(
                __scrape_office_enhanced(driver, scraping_config, location_link),
                ["name", "address"],
            )
            offices.append(office)
    finally:
        if driver:
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
    __scroll(driver)

    wait_element_timeout = scraping_config["wait_element_timeout"]
    try:
        # It seems that more time is need to wait for the address to appear.
        office_address_p = WebDriverWait(driver, wait_element_timeout * 6).until(
            html_text_has_been_added((By.XPATH, "/descendant::figure[2]//p[2]"))
        )
    except:
        logger.info(f"Can't get the address of the office: {name}")
    else:
        address = office_address_p.text
    finally:
        driver.close()
        driver.switch_to.window(current_window_handle)

    return (
        name,
        address,
    )


def __scroll(driver):
    """Scroll to the element used to show the office address.
    The scrolling is required becuase the element used to show the office address
    won't be loaded until the page is scrolled to make it being in the viewport.
    """
    y_coord = driver.execute_script(
        """
        var section = document.querySelector('main > content > section:nth-child(2)');
        return section ? section.offsetTop : 0;
    """
    )
    driver.execute_script("window.scrollTo(0, {})".format(y_coord))