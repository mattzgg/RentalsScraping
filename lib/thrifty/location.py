import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from ..utils import constants
from ..utils.web_scraping import wait_elements_until_visible_by_css_selector


def scrape_offices(scraping_config):
    """Returns a list of office objects scraped from the Thrifty's locations page.
    An office object is composed of a name and address.
    """
    logger = logging.getLogger(__name__)

    logger.info("Scraping Thrifty's offices begins.")
    headless = scraping_config["headless"]
    wait_element_timeout = scraping_config["wait_element_timeout"]
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    logger.info("Selenium driver is ready.")
    driver.get(constants.THRIFTY_COMPANY_LOCATIONS_PAGE_URL)
    logger.info(f"Selenium driver opens {constants.THRIFTY_BOOKING_PAGE_URL}")

    try:
        catalogue_content_wrapper_css_selector = ".catalogue__content-wrapper"
        wait_elements_until_visible_by_css_selector(
            driver,
            wait_element_timeout,
            catalogue_content_wrapper_css_selector,
        )
        logger.info("Offices are available now.")
        offices = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        catalogue_content_wrappers = soup.select(catalogue_content_wrapper_css_selector)
        for catalogue_content_wrapper in catalogue_content_wrappers:
            name = str(catalogue_content_wrapper.h2.string)
            address = str(catalogue_content_wrapper.div.p.string)
            offices.append({"name": name, "address": address})
            logger.info(f"The office[name: {name}, address: {address}] is obtained.")
        logger.info("Scraping Thrifty's offices is finished.")
    finally:
        if driver:
            driver.quit()

    return offices
