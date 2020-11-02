from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from ..utils import constants
from ..utils.web_scraping import wait_elements_until_visible_by_css_selector


def scrape_offices():
    """Returns a list of office objects scraped from the Thrifty's locations page.
    An office object is composed of a name and address.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(constants.THRIFTY_COMPANY_LOCATIONS_PAGE_URL)

    catalogue_content_wrapper_css_selector = ".catalogue__content-wrapper"
    wait_elements_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, catalogue_content_wrapper_css_selector
    )

    offices = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    catalogue_content_wrappers = soup.select(catalogue_content_wrapper_css_selector)
    for catalogue_content_wrapper in catalogue_content_wrappers:
        name = str(catalogue_content_wrapper.h2.string)
        address = str(catalogue_content_wrapper.div.p.string)
        offices.append({"name": name, "address": address})

    driver.quit()

    return offices
