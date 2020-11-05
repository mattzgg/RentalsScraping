import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ..utils import constants
from ..utils.web_scraping import (
    wait_element_until_visible_by_css_selector,
    wait_element_until_visible_by_xpath,
    focus_element,
    parse_date_text,
)


def scrape_quotes(non_fulfilled_booking_request):
    company_id = non_fulfilled_booking_request["company_id"]
    rental_route_id = non_fulfilled_booking_request["rental_route_id"]
    pick_up_date_id = non_fulfilled_booking_request["pick_up_date_id"]
    pick_up_time_id = non_fulfilled_booking_request["pick_up_time_id"]
    rental_duration_id = non_fulfilled_booking_request["rental_duration_id"]
    pick_up_office_name = non_fulfilled_booking_request["pick_up_office_name"]
    pick_up_office_address = non_fulfilled_booking_request["pick_up_office_address"]
    drop_off_office_name = non_fulfilled_booking_request["drop_off_office_name"]
    drop_off_office_address = non_fulfilled_booking_request["drop_off_office_address"]
    pick_up_date_value = non_fulfilled_booking_request["pick_up_date_value"]
    pick_up_time_value = non_fulfilled_booking_request["pick_up_time_value"]
    drop_off_date_value = non_fulfilled_booking_request["drop_off_date_value"]
    drop_off_time_value = non_fulfilled_booking_request["drop_off_time_value"]

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(constants.BUDGET_BOOKING_PAGE_URL)

    fill_location_input(driver, "#PicLoc_value", pick_up_office_address)
    fill_location_input(driver, "#DropLoc_value", drop_off_office_address)
    fill_date_input(driver, "#from", pick_up_date_value)
    fill_time_input(driver, "reservationModel.pickUpTime", pick_up_time_value)
    fill_date_input(driver, "#to", drop_off_date_value)
    fill_time_input(driver, "reservationModel.dropTime", drop_off_time_value)

    click_select_my_vehicle_button(driver)

    driver.quit()


def fill_location_input(driver, input_css_selector, input_value):
    location_input = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, input_css_selector
    )
    location_input.send_keys(input_value)

    try:
        suggested_location_element = WebDriverWait(
            driver, constants.SCRAPE_TIMEOUT
        ).until(presence_of_match_from_suggested_locations(input_value))
    except TimeoutException:
        raise RuntimeError(
            "Cannot find suggested location for the location input["
            + input_css_selector
            + "] on the page."
        )
    else:
        suggested_location_element.click()


class presence_of_match_from_suggested_locations:
    def __init__(self, input_value):
        self.input_value = input_value

    def __call__(self, driver):
        suggested_locations = driver.find_elements(
            By.CSS_SELECTOR, ".angucomplete-description"
        )
        if suggested_locations:
            for suggested_location in suggested_locations:
                if suggested_location.text == self.input_value:
                    return suggested_location
            return False
        else:
            return False


def click_select_my_vehicle_button(driver):
    select_my_vehicle_button = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, "#res-home-select-car"
    )
    select_my_vehicle_button.click()


def fill_date_input(driver, input_css_selector, input_value):
    def parse_month_year_text(month_year_text):
        items = month_year_text.split(" ")
        month_text = items[0]
        year_text = items[1]
        return {"month": constants.MONTHS[month_text.upper()], "year": int(year_text)}

    def calc_number_of_months(month_year):
        return month_year["year"] * 12 + month_year["month"]

    def compare_month_year(month_year_1, month_year_2):
        number_of_month_1 = calc_number_of_months(month_year_1)
        number_of_month_2 = calc_number_of_months(month_year_2)
        return number_of_month_1 - number_of_month_2

    # Open the date picker.
    date_input = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, input_css_selector
    )
    focus_element(driver, date_input)

    current_date = parse_date_text(input_value)

    # Calculate the parameters required to decide whether to adjust the date picker.
    left_month_year_label = wait_element_until_visible_by_css_selector(
        driver,
        constants.SCRAPE_TIMEOUT,
        ".ui-datepicker-group-first .ui-datepicker-title",
    )
    left_month_year = parse_month_year_text(left_month_year_label.text)
    right_month_year_label = wait_element_until_visible_by_css_selector(
        driver,
        constants.SCRAPE_TIMEOUT,
        ".ui-datepicker-group-last .ui-datepicker-title",
    )
    right_month_year = parse_month_year_text(right_month_year_label.text)
    current_month_year = {
        "month": current_date["month"],
        "year": current_date["year"],
    }
    left_difference = compare_month_year(current_month_year, left_month_year)
    right_difference = compare_month_year(current_month_year, right_month_year)

    # Adjust the date picker to make it dispaly proper dates which include the current date
    if left_difference < 0:
        prev_counter = 0
        step_count = abs(left_difference)
        while prev_counter < step_count:
            prev_link = wait_element_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                ".ui-datepicker-prev",
            )
            prev_link.click()
            prev_counter += 1
    elif right_difference > 0:
        next_counter = 0
        step_count = abs(right_difference)
        while next_counter < step_count:
            next_link = wait_element_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                ".ui-datepicker-next",
            )
            next_link.click()
            next_counter += 1

    # Select the current date
    day_text = str(current_date["day"])
    if left_difference <= 0:
        day_link_xpath = (
            "//table[contains(normalize-space(@class), 'ui-datepicker-table-first')]//td[a="
            + day_text
            + "]/a"
        )
        day_link = wait_element_until_visible_by_xpath(
            driver, constants.SCRAPE_TIMEOUT, day_link_xpath
        )
        day_link.click()
    elif right_difference >= 0:
        day_link_xpath = (
            "//table[contains(normalize-space(@class), 'ui-datepicker-table-last')]//td[a="
            + day_text
            + "]/a"
        )
        day_link = wait_element_until_visible_by_xpath(
            driver, constants.SCRAPE_TIMEOUT, day_link_xpath
        )
        day_link.click()


def fill_time_input(driver, input_name, input_value):
    time_select_xpath = "//select[@name='" + input_name + "']"
    time_select = wait_element_until_visible_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        time_select_xpath,
    )
    time_select.click()

    if input_value == "12:00 AM":
        input_value = "midnight"
    elif input_value == "12:00 PM":
        input_value = "noon"
    input_value = input_value.lstrip("0")
    time_option_xpath = time_select_xpath + "/option[@label='" + input_value + "']"
    time_option = wait_element_until_visible_by_xpath(
        driver, constants.SCRAPE_TIMEOUT, time_option_xpath
    )
    time_option.click()
