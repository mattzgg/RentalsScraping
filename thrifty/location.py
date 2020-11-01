from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from utils import constants


def scrape_locations():
    """Returns a list of location objects scraped from the Thrifty's locations page.
    A location object composes a name and an address.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(constants.THRIFTY_COMPANY_LOCATIONS_PAGE_URL)

    locations = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    catalogue_content_wrappers = soup.select(".catalogue__content-wrapper")
    for catalogue_content_wrapper in catalogue_content_wrappers:
        location_name = str(catalogue_content_wrapper.h2.string)
        location_address = str(catalogue_content_wrapper.div.p.string)
        locations.append({"name": location_name, "address": location_address})

    driver.quit()

    return locations
