from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from ..utils import constants
from ..utils.data_processing import assemble_quotes
from ..utils.web_scraping import (
    wait_dom_ready,
    wait_element_until_visible_by_xpath,
    wait_element_until_visible_by_css_selector,
    wait_elements_until_visible_by_css_selector,
    parse_date_text,
    check_if_element_has_class,
    extract_price,
    parse_month_year_text,
    compare_month_year,
    raise_date_is_not_spported,
    add_months_to_month_year,
)
from ..utils.exceptions import QuotesNotAvailableException


def scrape_quotes(driver, scraping_config, scraping_request):
    wait_element_timeout = scraping_config["wait_element_timeout"]
    dom_ready_timeout = scraping_config["dom_ready_timeout"]

    def normalize_office_name(office_name):
        # Normalization is required because some location names on the Locations page
        # are different from the counterparts used in the location select.
        return office_name.replace("–", "-")

    def normalize_time_value(time_value):
        return time_value.lower().lstrip("0")

    pick_up_office_name = normalize_office_name(scraping_request["pick_up_office_name"])
    drop_off_office_name = normalize_office_name(
        scraping_request["drop_off_office_name"]
    )
    pick_up_date_value = scraping_request["pick_up_date_value"]
    pick_up_time_value = normalize_time_value(scraping_request["pick_up_time_value"])
    drop_off_date_value = scraping_request["drop_off_date_value"]
    drop_off_time_value = normalize_time_value(scraping_request["drop_off_time_value"])

    driver.get(constants.THRIFTY_BOOKING_PAGE_URL)
    wait_dom_ready(driver, dom_ready_timeout)

    __fill_select(driver, scraping_config, "pickup-depot", pick_up_office_name)
    __fill_select(driver, scraping_config, "return-depot", drop_off_office_name)
    __fill_date_input(driver, scraping_config, "pickup-date", pick_up_date_value)
    __fill_select(driver, scraping_config, "pickup-time", pick_up_time_value)
    __fill_date_input(driver, scraping_config, "return-date", drop_off_date_value)
    __fill_select(driver, scraping_config, "return-time", drop_off_time_value)

    # Click the Find a Vehicle button
    find_a_vehicle_button = wait_element_until_visible_by_css_selector(
        driver, wait_element_timeout, "#find_vehicle"
    )
    find_a_vehicle_button.click()
    wait_dom_ready(driver, dom_ready_timeout)

    quotes = assemble_quotes(scraping_request, [])
    try:
        wait_elements_until_visible_by_css_selector(
            driver,
            wait_element_timeout,
            ".booking-steps__content .vehicle",
        )
    except:
        raise QuotesNotAvailableException(scraping_request)
    else:
        quotes = __parse_find_a_vehicle_response(driver, scraping_request)

    return quotes


def __fill_select(driver, scraping_config, location_input_id, location_input_value):
    wait_element_timeout = scraping_config["wait_element_timeout"]
    location_input_css_selector = "#select2-{}-container".format(location_input_id)
    location_input = wait_element_until_visible_by_css_selector(
        driver, wait_element_timeout, location_input_css_selector
    )
    location_input.click()

    location_option_xpath = (
        "//span[contains(@class, '{}')]//ul/li[normalize-space(text())='{}']".format(
            location_input_id, location_input_value
        )
    )
    location_option = wait_element_until_visible_by_xpath(
        driver, wait_element_timeout, location_option_xpath
    )
    location_option.click()


def __fill_date_input(driver, scraping_config, date_input_id, date_value):
    wait_element_timeout = scraping_config["wait_element_timeout"]

    def calculate_month_year_difference(driver, target_month_year):
        """Calculate the difference required to decide whether to adjust the date picker."""
        current_month_label_css_selector = "#{}_root .picker__month".format(
            date_input_id
        )
        current_month_label = wait_element_until_visible_by_css_selector(
            driver, wait_element_timeout, current_month_label_css_selector
        )
        current_month_label_text = current_month_label.text
        current_year_label_css_selector = "#{}_root .picker__year".format(date_input_id)
        current_year_label = wait_element_until_visible_by_css_selector(
            driver, wait_element_timeout, current_year_label_css_selector
        )
        current_year_label_text = current_year_label.text
        current_month_year = parse_month_year_text(
            "{} {}".format(current_month_label_text, current_year_label_text)
        )
        difference = compare_month_year(target_month_year, current_month_year)
        return difference

    class target_month_year_to_be_visible:
        def __init__(self, target_month_year):
            self.target_month_year = target_month_year

        def __call__(self, driver):
            return calculate_month_year_difference(driver, self.target_month_year) == 0

    def wait_for_target_month_year_to_show(target_month_year):
        # Wait for target month year, or an stale element exception occurs.
        WebDriverWait(driver, wait_element_timeout).until(
            target_month_year_to_be_visible(target_month_year)
        )

    # Open the date picker.
    date_input_css_selector = "#{}".format(date_input_id)
    date_input = wait_element_until_visible_by_css_selector(
        driver, wait_element_timeout, date_input_css_selector
    )
    date_input.click()

    date_dmy = parse_date_text(date_value)
    target_month_year = {
        "month": date_dmy["month"],
        "year": date_dmy["year"],
    }
    difference = calculate_month_year_difference(driver, target_month_year)

    # Adjust the date picker to make it display proper dates which include the current date.
    if difference < 0:
        prev_counter = 1
        step_count = abs(difference)
        prev_link_css_selector = "#{}_root .picker__nav--prev".format(date_input_id)
        while prev_counter <= step_count:
            prev_link = wait_element_until_visible_by_css_selector(
                driver,
                wait_element_timeout,
                prev_link_css_selector,
            )
            is_prev_link_disabled = check_if_element_has_class(
                prev_link, "picker__nav--disabled"
            )
            if is_prev_link_disabled:
                raise_date_is_not_spported(date_value)
            prev_link.click()

            number_of_months_added = step_count - prev_counter
            temp_target_month_year = add_months_to_month_year(
                target_month_year, number_of_months_added
            )
            wait_for_target_month_year_to_show(temp_target_month_year)

            prev_counter += 1
    elif difference > 0:
        next_counter = 1
        step_count = difference
        next_link_css_selector = "#{}_root .picker__nav--next".format(date_input_id)
        while next_counter <= step_count:
            next_link = wait_element_until_visible_by_css_selector(
                driver,
                wait_element_timeout,
                next_link_css_selector,
            )
            is_next_link_disabled = check_if_element_has_class(
                next_link, "picker__nav--disabled"
            )
            if is_next_link_disabled:
                raise_date_is_not_spported(date_value)
            next_link.click()

            number_of_months_added = -(step_count - next_counter)
            temp_target_month_year = add_months_to_month_year(
                target_month_year, number_of_months_added
            )
            wait_for_target_month_year_to_show(temp_target_month_year)

            next_counter += 1

    # Select the current date
    day_text = str(date_dmy["day"])
    day_link_xpath = (
        "//div[@id='{}_root']//div[contains(@class, 'picker__day') "
        + "and contains(@class, 'picker__day--infocus') "
        + "and normalize-space(text())='{}']"
    ).format(date_input_id, day_text)
    day_link = wait_element_until_visible_by_xpath(
        driver, wait_element_timeout, day_link_xpath
    )
    day_link_class = day_link.get_attribute("class")
    if "picker__day--disabled" in day_link_class:
        raise_date_is_not_spported(date_value)
    day_link.click()


def __parse_find_a_vehicle_response(driver, scraping_request):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    vehicle_elements = soup.select(".booking-steps__content .vehicle")
    scraping_response = []
    for vehicle_element in vehicle_elements:
        vehicle_category_name = str(
            vehicle_element.select_one("p.vehicle__p > strong").string
        )
        price_element = vehicle_element.select_one("span.vehicle__total > span.text")
        price = None
        if price_element:
            price_text = str(price_element.string)
            price = extract_price(price_text)
        # For Thrifty, vehicle category description and vehicle age description are optional
        scraping_response.append(
            {
                "vehicle_category_name": vehicle_category_name,
                "vehicle_category_description": "",
                "vehicle_age_description": "",
                "price": price,
            }
        )
    quotes = assemble_quotes(scraping_request, scraping_response)
    return quotes
