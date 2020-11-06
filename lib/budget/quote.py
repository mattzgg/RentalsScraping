import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ..utils import constants
from ..utils.web_scraping import (
    wait_element_until_visible_by_css_selector,
    wait_elements_until_visible_by_css_selector,
    wait_element_until_visible_by_xpath,
    focus_element,
    parse_date_text,
    extract_price,
)
from ..utils.ui import create_warning, create_error


def scrape_quotes(non_fulfilled_booking_request):
    driver = None
    quotes = []

    try:
        pick_up_office_name = non_fulfilled_booking_request["pick_up_office_name"]
        pick_up_office_address = non_fulfilled_booking_request["pick_up_office_address"]
        drop_off_office_name = non_fulfilled_booking_request["drop_off_office_name"]
        drop_off_office_address = non_fulfilled_booking_request[
            "drop_off_office_address"
        ]
        pick_up_date_value = non_fulfilled_booking_request["pick_up_date_value"]
        pick_up_time_value = non_fulfilled_booking_request["pick_up_time_value"]
        drop_off_date_value = non_fulfilled_booking_request["drop_off_date_value"]
        drop_off_time_value = non_fulfilled_booking_request["drop_off_time_value"]

        chrome_options = Options()
        if constants.IS_CHROME_HEADLESS_ENABLED:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(constants.BUDGET_BOOKING_PAGE_URL)

        __fill_location_input(
            driver, "#PicLoc_value", pick_up_office_name, pick_up_office_address
        )
        __fill_location_input(
            driver, "#DropLoc_value", drop_off_office_name, drop_off_office_address
        )
        __fill_date_input(driver, "#from", pick_up_date_value)
        __fill_time_input(driver, "reservationModel.pickUpTime", pick_up_time_value)
        __fill_date_input(driver, "#to", drop_off_date_value)
        __fill_time_input(driver, "reservationModel.dropTime", drop_off_time_value)

        __click_select_my_vehicle_button(driver)

        try:
            quotes = __scrape_quotes_on_page(driver)
        except TimeoutException as exception:
            warning = create_warning(
                "\nNo quotes were found for the non-fulfilled booking request:\n{}".format(
                    pprint.pformat(non_fulfilled_booking_request)
                )
            )
            print(warning)
    finally:
        if driver:
            driver.quit()

    return quotes


def __fill_location_input(driver, input_css_selector, office_name, office_address):
    location_input = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, input_css_selector
    )
    location_input_value = constants.BUDGET_LOCATION_INPUT_VALUE_DICT[office_name]
    location_input.send_keys(location_input_value)

    try:
        suggested_location_element = WebDriverWait(
            driver, constants.SCRAPE_TIMEOUT
        ).until(presence_of_match_from_suggested_locations(office_address))
    except TimeoutException:
        raise Exception(
            "Budget > Fill location input '{}': No suggestion found for '{}/{}'".format(
                input_css_selector, office_name, office_address
            )
        )
    else:
        suggested_location_element.click()


class presence_of_match_from_suggested_locations:
    def __init__(self, office_address):
        self.office_address = office_address

    def __call__(self, driver):
        suggested_locations = driver.find_elements(
            By.CSS_SELECTOR, ".angucomplete-description"
        )
        if suggested_locations:
            for suggested_location in suggested_locations:
                if suggested_location.text == self.office_address:
                    return suggested_location
            return False
        else:
            return False


def __click_select_my_vehicle_button(driver):
    select_my_vehicle_button = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, "#res-home-select-car"
    )
    select_my_vehicle_button.click()


def __fill_date_input(driver, input_css_selector, input_value):
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

    # Adjust the date picker to make it display proper dates which include the current date.
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
        step_count = right_difference
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


def __fill_time_input(driver, input_name, input_value):
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


def __scrape_quotes_on_page(driver):
    vehicle_category_list = wait_elements_until_visible_by_css_selector(
        driver,
        constants.SCRAPE_TIMEOUT,
        ".avilablecar.available-car-box .avilcardtl h3",
    )
    vehicle_price_list = wait_elements_until_visible_by_css_selector(
        driver,
        constants.SCRAPE_TIMEOUT,
        ".avilablecar.available-car-box .payamntr price",
    )
    vehicle_category_count = len(vehicle_category_list)
    vehicle_price_count = len(vehicle_price_list)
    # Some vehicles show without a price.
    assert vehicle_category_count >= vehicle_price_count

    quotes = []
    index = 0
    for vehicle_category in vehicle_category_list:
        if index == vehicle_price_count:
            break

        vehicle_price = vehicle_price_list[index]
        vehicle_price_decimal = extract_price(vehicle_price.text)
        # For Budget, vehicle category description and vehicle age description are optional
        quotes.append(
            {
                "vehicle_category_name_in_company": vehicle_category.text,
                "vehicle_category_description": "",
                "vehicle_age_description": "",
                "price": vehicle_price_decimal,
            }
        )
        index = index + 1

    return quotes