from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from utils import constants


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

    soup = BeautifulSoup(driver.page_source, "html.parser")
    location_element_css_selector = locations_container_css_selector + " li a"
    location_elements = soup.select(location_element_css_selector)
    location_names = []
    for location_element in location_elements:
        location_name = str(location_element.string)
        location_names.append(location_name)

    driver.quit()

    return location_names
