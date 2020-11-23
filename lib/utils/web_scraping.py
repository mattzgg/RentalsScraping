import time, random, re, math

from datetime import datetime
from decimal import Decimal
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sys import platform
from . import constants
from .datatype import is_empty_string


class html_input_has_value:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element and not is_empty_string(element.get_attribute("value")):
            return element
        else:
            return False


class html_text_has_been_added:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element and not is_empty_string(element.text):
            return element
        else:
            return False


def with_random_delay(func, min_delay=0, max_delay=5):
    def new_func(*args):
        result = func(*args)
        random_delay = random.randint(min_delay, max_delay)
        time.sleep(random_delay)
        return result

    return new_func


def is_mac_os():
    return platform == "darwin"


def open_link_in_new_tab(html_link):
    modifier_key = Keys.COMMAND if is_mac_os() else Keys.CONTROL
    html_link.send_keys(modifier_key, Keys.RETURN)


def wait_dom_ready(driver, timeout):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def wait_element_until_visible_by_css_selector(driver, timeout, css_selector):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
    )


def wait_element_until_visible_by_id(driver, timeout, id):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, id))
    )


def wait_elements_until_visible_by_css_selector(driver, timeout, css_selector):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )


def wait_element_until_visible_by_xpath(driver, timeout, xpath):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def wait_elements_until_visible_by_xpath(driver, timeout, xpath):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_all_elements_located((By.XPATH, xpath))
    )


def wait_element_until_present_by_xpath(driver, timeout, xpath):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def focus_element(driver, element):
    if element.tag_name == "input":
        element.send_keys("")
    else:
        ActionChains(driver).moveToElement(element).perform()


def parse_date_text(date_text):
    """Parse a date string with format %d/%m/%Y to a dictionary of day, month and year,
    e.g., parse '04/11/2020' to {"day": 4, "month": 11, "year": 2020}
    """
    dmy = date_text.split("/")
    return {"day": int(dmy[0]), "month": int(dmy[1]), "year": int(dmy[2])}


def time_until_end_of_day(dt=None):
    """Get timedelta in seconds until end of day on the datetime passed, or current time."""
    if dt is None:
        dt = datetime.now()
    return (
        ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)
    )


def extract_price(quote_text):
    price = 0

    quote_text = quote_text.replace(",", "")  # Remove the thousand separator
    pattern = re.compile("\d+(\.\d{2})?")
    match_object = pattern.search(quote_text)
    if match_object:
        price_text = match_object.group(0)
        price = Decimal(price_text)

    return price


def check_if_element_has_class(element, specific_class):
    element_class = element.get_attribute("class")
    return specific_class in element_class


def join_bs4_strings(bs4_element, separator=""):
    bs4_strings = bs4_element.strings
    strings = map(str, bs4_strings)
    return separator.join(strings)


def parse_month_year_text(month_year_text):
    """A month year text matches the MONTH YEAR pattern, e.g. November 2020"""
    items = month_year_text.split(" ")
    month_text = items[0]
    year_text = items[1]
    return {"month": constants.MONTHS[month_text.upper()], "year": int(year_text)}


def calc_number_of_months(month_year):
    return month_year["year"] * 12 + month_year["month"]


def compare_month_year(month_year_1, month_year_2):
    number_of_months_1 = calc_number_of_months(month_year_1)
    number_of_months_2 = calc_number_of_months(month_year_2)
    return number_of_months_1 - number_of_months_2


def add_months_to_month_year(month_year, number_of_months_added):
    number_of_months = calc_number_of_months(month_year)
    new_number_of_months = number_of_months + number_of_months_added
    month = new_number_of_months % 12
    year = math.floor(new_number_of_months / 12)
    if month == 0:
        month = 12
        year = year - 1
    return {
        "month": month,
        "year": year,
    }


def raise_date_is_not_spported(date_value):
    raise RuntimeError("The date {} is not supported.".format(date_value))


def assemble_quotes(scraping_request, scraping_response):
    """A quote is composed of a head and a body. The data of the head comes from a scraping
    request. The data of the body comes from a scrapng response."""

    def is_meaningful_price(quote_body):
        price = quote_body["price"]
        return price is not None

    quotes = []

    quote_head = {
        "company_id": scraping_request["company_id"],
        "rental_route_id": scraping_request["rental_route_id"],
        "pick_up_date_id": scraping_request["pick_up_date_id"],
        "pick_up_time_id": scraping_request["pick_up_time_id"],
        "rental_duration_id": scraping_request["rental_duration_id"],
        "created_on": datetime.now(),
    }

    scraping_response = list(filter(is_meaningful_price, scraping_response))

    if len(scraping_response) == 0:
        quotes.append({**quote_head})
    else:
        for quote_body in scraping_response:
            quote = {**quote_head, **quote_body}
            quotes.append(quote)

    return quotes
