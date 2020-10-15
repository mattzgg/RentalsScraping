import time
import random


from selenium.webdriver.common.keys import Keys
from utils.datatype import is_empty_string
from sys import platform


class html_input_has_value:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element and not is_empty_string(element.get_attribute("value")):
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