import time, pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..utils import constants
from ..utils.web_scraping import (
    wait_element_until_present_by_xpath,
    wait_element_until_visible_by_xpath,
    wait_element_until_visible_by_css_selector,
    wait_elements_until_visible_by_css_selector,
    parse_date_text,
    check_if_element_has_class,
    extract_price,
)
from ..utils.ui import create_warning


def scrape_quotes(non_fulfilled_booking_request):
    def normalize_office_name(office_name):
        # Normalization is required because some location names on the Locations page
        # are different from the counterparts used in the location select.
        return office_name.replace("–", "-")

    def normalize_time_value(time_value):
        return time_value.lower().lstrip("0")

    driver = None
    quotes = []

    try:
        pick_up_office_name = normalize_office_name(
            non_fulfilled_booking_request["pick_up_office_name"]
        )
        pick_up_office_address = non_fulfilled_booking_request["pick_up_office_address"]
        drop_off_office_name = normalize_office_name(
            non_fulfilled_booking_request["drop_off_office_name"]
        )
        drop_off_office_address = non_fulfilled_booking_request[
            "drop_off_office_address"
        ]
        pick_up_date_value = non_fulfilled_booking_request["pick_up_date_value"]
        pick_up_time_value = normalize_time_value(
            non_fulfilled_booking_request["pick_up_time_value"]
        )
        drop_off_date_value = non_fulfilled_booking_request["drop_off_date_value"]
        drop_off_time_value = normalize_time_value(
            non_fulfilled_booking_request["drop_off_time_value"]
        )

        chrome_options = Options()
        if constants.IS_CHROME_HEADLESS_ENABLED:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(constants.THRIFTY_BOOKING_PAGE_URL)

        __fill_select(driver, "pickup-depot", pick_up_office_name)
        __fill_select(driver, "return-depot", drop_off_office_name)
        __fill_date_input(driver, "pickup-date", pick_up_date_value)
        __fill_select(driver, "pickup-time", pick_up_time_value)
        __fill_date_input(driver, "return-date", drop_off_date_value)
        __fill_select(driver, "return-time", drop_off_time_value)

        # Click the Find a Vehicle button
        find_a_vehicle_button = wait_element_until_visible_by_css_selector(
            driver, constants.SCRAPE_TIMEOUT, "#find_vehicle"
        )
        find_a_vehicle_button.click()

        try:
            wait_elements_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                ".booking-steps__content .vehicle",
            )
        except TimeoutException as exception:
            warning = create_warning(
                "\nNo quotes were found for the non-fulfilled booking request:\n{}".format(
                    pprint.pformat(non_fulfilled_booking_request)
                )
            )
            print(warning)
        else:
            quotes = __scrape_quotes_on_page(driver)
    finally:
        if driver:
            driver.quit()

    return quotes


def __fill_select(driver, location_input_id, location_input_value):
    location_input_css_selector = "#select2-{}-container".format(location_input_id)
    location_input = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, location_input_css_selector
    )
    location_input.click()

    location_option_xpath = (
        "//span[contains(@class, '{}')]//ul/li[normalize-space(text())='{}']".format(
            location_input_id, location_input_value
        )
    )
    location_option = wait_element_until_visible_by_xpath(
        driver, constants.SCRAPE_TIMEOUT, location_option_xpath
    )
    location_option.click()


def __fill_date_input(driver, date_input_id, date_value):
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

    def raise_date_is_not_spported():
        raise RuntimeError("The date {} is not supported.".format(date_value))

    # Open the date picker.
    date_input_css_selector = "#{}".format(date_input_id)
    date_input = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, date_input_css_selector
    )
    date_input.click()

    current_date = parse_date_text(date_value)

    # Calculate the parameters required to decide whether to adjust the date picker.
    month_label_css_selector = "#{}_root .picker__month".format(date_input_id)
    month_label = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, month_label_css_selector
    )
    month_label_text = month_label.text
    year_label_css_selector = "#{}_root .picker__year".format(date_input_id)
    year_label = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, year_label_css_selector
    )
    year_label_text = year_label.text
    month_year = parse_month_year_text(
        "{} {}".format(month_label_text, year_label_text)
    )
    current_month_year = {
        "month": current_date["month"],
        "year": current_date["year"],
    }
    difference = compare_month_year(current_month_year, month_year)

    # Adjust the date picker to make it display proper dates which include the current date.
    if difference < 0:
        prev_counter = 0
        step_count = abs(difference)
        prev_link_css_selector = "#{}_root .picker__nav--prev".format(date_input_id)
        while prev_counter < step_count:
            prev_link = wait_element_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                prev_link_css_selector,
            )
            is_prev_link_disabled = check_if_element_has_class(
                prev_link, "picker__nav--disabled"
            )
            if is_prev_link_disabled:
                raise_date_is_not_spported()
            prev_link.click()
            prev_counter += 1
    elif difference > 0:
        next_counter = 0
        step_count = difference
        next_link_css_selector = "#{}_root .picker__nav--next".format(date_input_id)
        while next_counter < step_count:
            next_link = wait_element_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                next_link_css_selector,
            )
            is_next_link_disabled = check_if_element_has_class(
                next_link, "picker__nav--disabled"
            )
            if is_next_link_disabled:
                raise_date_is_not_spported()
            next_link.click()
            next_counter += 1

    # Select the current date
    day_text = str(current_date["day"])
    day_link_xpath = (
        "//div[@id='{}_root']//div[contains(@class, 'picker__day') "
        + "and contains(@class, 'picker__day--infocus') "
        + "and normalize-space(text())='{}']"
    ).format(date_input_id, day_text)
    day_link = wait_element_until_visible_by_xpath(
        driver, constants.SCRAPE_TIMEOUT, day_link_xpath
    )
    day_link_class = day_link.get_attribute("class")
    if "picker__day--disabled" in day_link_class:
        raise_date_is_not_spported()
    day_link.click()


def __scrape_quotes_on_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    vehicle_elements = soup.select(".booking-steps__content .vehicle")
    quotes = []
    for vehicle_element in vehicle_elements:
        vehicle_category_name_in_company = str(
            vehicle_element.select_one("p.vehicle__p > strong").string
        )
        price_element = vehicle_element.select_one("span.vehicle__total > span.text")
        price_text = str(price_element.string) if price_element else "0.00"
        price = extract_price(price_text)
        # For Thrifty, vehicle category description and vehicle age description are optional
        quotes.append(
            {
                "vehicle_category_name_in_company": vehicle_category_name_in_company,
                "vehicle_category_description": "",
                "vehicle_age_description": "",
                "price": price,
            }
        )
    return quotes
