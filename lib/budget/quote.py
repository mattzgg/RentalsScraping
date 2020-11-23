from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from ..utils import constants
from ..utils.web_scraping import (
    wait_dom_ready,
    wait_element_until_visible_by_css_selector,
    wait_elements_until_visible_by_css_selector,
    wait_element_until_visible_by_xpath,
    focus_element,
    parse_date_text,
    extract_price,
    join_bs4_strings,
    parse_month_year_text,
    compare_month_year,
    raise_date_is_not_spported,
    add_months_to_month_year,
    check_if_element_has_class,
    assemble_quotes,
)
from ..utils.exceptions import QuotesNotAvailableException


def scrape_quotes(driver, scraping_request):
    pick_up_office_name = scraping_request["pick_up_office_name"]
    pick_up_office_address = scraping_request["pick_up_office_address"]
    drop_off_office_name = scraping_request["drop_off_office_name"]
    drop_off_office_address = scraping_request["drop_off_office_address"]
    pick_up_date_value = scraping_request["pick_up_date_value"]
    pick_up_time_value = scraping_request["pick_up_time_value"]
    drop_off_date_value = scraping_request["drop_off_date_value"]
    drop_off_time_value = scraping_request["drop_off_time_value"]

    driver.get(constants.BUDGET_BOOKING_PAGE_URL)
    wait_dom_ready(driver, constants.DOM_READY_TIMEOUT)

    __fill_location_input(
        driver, "PicLoc_value", pick_up_office_name, pick_up_office_address
    )
    __fill_location_input(
        driver, "DropLoc_value", drop_off_office_name, drop_off_office_address
    )
    __fill_date_input(driver, "from", pick_up_date_value)
    __fill_time_select(driver, "reservationModel.pickUpTime", pick_up_time_value)
    __fill_date_input(driver, "to", drop_off_date_value)
    __fill_time_select(driver, "reservationModel.dropTime", drop_off_time_value)

    # Click the Select My Vehicle button
    select_my_vehicle_button = wait_element_until_visible_by_css_selector(
        driver, constants.WAIT_ELEMENT_TIMEOUT, "#res-home-select-car"
    )
    select_my_vehicle_button.click()
    wait_dom_ready(driver, constants.DOM_READY_TIMEOUT)

    quotes = assemble_quotes(scraping_request, [])
    try:
        wait_elements_until_visible_by_css_selector(
            driver,
            constants.WAIT_ELEMENT_TIMEOUT,
            ".available-car-box",
        )
    except:
        raise QuotesNotAvailableException(scraping_request)
    else:
        quotes = __parse_select_my_vehicle_response(driver, scraping_request)

    return quotes


def __fill_location_input(driver, location_input_id, office_name, office_address):
    location_input_css_selector = "#{}".format(location_input_id)
    location_input = wait_element_until_visible_by_css_selector(
        driver, constants.WAIT_ELEMENT_TIMEOUT, location_input_css_selector
    )
    location_input_value = constants.BUDGET_LOCATION_INPUT_VALUE_DICT[office_name]
    location_input.clear()
    location_input.send_keys(location_input_value)

    office_address_element = WebDriverWait(
        driver, constants.WAIT_ELEMENT_TIMEOUT
    ).until(visibility_of_office_address_element(office_address))
    office_address_element.click()


class visibility_of_office_address_element:
    def __init__(self, office_address):
        self.office_address = office_address

    def __call__(self, driver):
        suggested_location_elements = driver.find_elements_by_css_selector(
            ".angucomplete-description"
        )
        if suggested_location_elements:
            for suggested_location_element in suggested_location_elements:
                if suggested_location_element.text == self.office_address:
                    return suggested_location_element
            return False
        else:
            return False


def __fill_date_input(driver, date_input_id, date_value):
    def calculate_month_year_difference(
        driver, current_month_year_label_css_selector, target_month_year
    ):
        """Calculate the difference required to decide whether to adjust the date picker."""
        current_month_year_label = wait_element_until_visible_by_css_selector(
            driver,
            constants.WAIT_ELEMENT_TIMEOUT,
            current_month_year_label_css_selector,
        )
        current_month_year = parse_month_year_text(current_month_year_label.text)
        difference = compare_month_year(target_month_year, current_month_year)
        return difference

    class target_month_year_to_be_visible:
        def __init__(self, current_month_year_label_css_selector, target_month_year):
            self.current_month_year_label_css_selector = (
                current_month_year_label_css_selector
            )
            self.target_month_year = target_month_year

        def __call__(self, driver):
            return (
                calculate_month_year_difference(
                    driver,
                    self.current_month_year_label_css_selector,
                    self.target_month_year,
                )
                == 0
            )

    def wait_for_target_month_year_to_show(
        current_month_year_label_css_selector, target_month_year
    ):
        # Wait for target month year, or an stale element exception occurs.
        WebDriverWait(driver, constants.WAIT_ELEMENT_TIMEOUT).until(
            target_month_year_to_be_visible(
                current_month_year_label_css_selector, target_month_year
            )
        )

    # Open the date picker.
    date_input_css_selector = "#{}".format(date_input_id)
    date_input = wait_element_until_visible_by_css_selector(
        driver, constants.WAIT_ELEMENT_TIMEOUT, date_input_css_selector
    )
    focus_element(driver, date_input)

    date_dmy = parse_date_text(date_value)
    target_month_year = {
        "month": date_dmy["month"],
        "year": date_dmy["year"],
    }

    left_current_month_year_label_css_selector = (
        ".ui-datepicker-group-first .ui-datepicker-title"
    )
    left_difference = calculate_month_year_difference(
        driver, left_current_month_year_label_css_selector, target_month_year
    )
    right_current_month_year_label_css_selector = (
        ".ui-datepicker-group-last .ui-datepicker-title"
    )
    right_difference = calculate_month_year_difference(
        driver, right_current_month_year_label_css_selector, target_month_year
    )

    # Adjust the date picker to make it display proper dates which include the current date.
    if left_difference < 0:
        prev_counter = 1
        step_count = abs(left_difference)
        while prev_counter <= step_count:
            prev_link = wait_element_until_visible_by_css_selector(
                driver,
                constants.WAIT_ELEMENT_TIMEOUT,
                ".ui-datepicker-prev",
            )
            is_prev_link_disabled = check_if_element_has_class(
                prev_link, "ui-state-disabled"
            )
            if is_prev_link_disabled:
                raise_date_is_not_spported(date_value)
            prev_link.click()

            number_of_months_added = step_count - prev_counter
            temp_target_month_year = add_months_to_month_year(
                target_month_year, number_of_months_added
            )
            wait_for_target_month_year_to_show(
                left_current_month_year_label_css_selector, temp_target_month_year
            )

            prev_counter += 1
    elif right_difference > 0:
        next_counter = 1
        step_count = right_difference
        while next_counter <= step_count:
            next_link = wait_element_until_visible_by_css_selector(
                driver,
                constants.WAIT_ELEMENT_TIMEOUT,
                ".ui-datepicker-next",
            )
            is_next_link_disabled = check_if_element_has_class(
                next_link, "ui-state-disabled"
            )
            if is_next_link_disabled:
                raise_date_is_not_spported(date_value)
            next_link.click()

            number_of_months_added = -(step_count - next_counter)
            temp_target_month_year = add_months_to_month_year(
                target_month_year, number_of_months_added
            )
            wait_for_target_month_year_to_show(
                right_current_month_year_label_css_selector, temp_target_month_year
            )

            next_counter += 1

    # Select the current date
    day_text = str(date_dmy["day"])
    if left_difference <= 0:
        day_link_xpath = (
            "//table[contains(@class, 'ui-datepicker-table-first')]//td[a='"
            + day_text
            + "']/a"
        )
        try:
            day_link = wait_element_until_visible_by_xpath(
                driver, constants.WAIT_ELEMENT_TIMEOUT, day_link_xpath
            )
        except:
            raise_date_is_not_spported(date_value)
        else:
            day_link.click()
    elif right_difference >= 0:
        day_link_xpath = (
            "//table[contains(@class, 'ui-datepicker-table-last')]//td[a='"
            + day_text
            + "']/a"
        )
        try:
            day_link = wait_element_until_visible_by_xpath(
                driver, constants.WAIT_ELEMENT_TIMEOUT, day_link_xpath
            )
        except:
            raise_date_is_not_spported(date_value)
        else:
            day_link.click()


def __fill_time_select(driver, time_select_name, time_value):
    time_select_xpath = "//select[@name='" + time_select_name + "']"
    time_select = wait_element_until_visible_by_xpath(
        driver,
        constants.WAIT_ELEMENT_TIMEOUT,
        time_select_xpath,
    )
    time_select.click()

    if time_value == "12:00 AM":
        time_value = "midnight"
    elif time_value == "12:00 PM":
        time_value = "noon"
    time_value = time_value.lstrip("0")
    time_option_xpath = time_select_xpath + "/option[@label='" + time_value + "']"
    time_option = wait_element_until_visible_by_xpath(
        driver, constants.WAIT_ELEMENT_TIMEOUT, time_option_xpath
    )
    time_option.click()


def __parse_select_my_vehicle_response(driver, scraping_request):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    available_car_boxes = soup.select(".available-car-box")
    scraping_response = []
    for available_car_box in available_car_boxes:
        vehicle_category_name_in_company = str(
            available_car_box.select_one("h3").string
        )
        price_element = available_car_box.select_one(".paynow price")
        price = None
        if price_element:
            price_text = join_bs4_strings(price_element)
            price = extract_price(price_text)
        # For Budget, vehicle category description and vehicle age description are optional
        scraping_response.append(
            {
                "vehicle_category_name_in_company": vehicle_category_name_in_company,
                "vehicle_category_description": "",
                "vehicle_age_description": "",
                "price": price,
            }
        )
    quotes = assemble_quotes(scraping_request, scraping_response)
    return quotes