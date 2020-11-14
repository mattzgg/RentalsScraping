import time, pprint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
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
    parse_month_year_text,
    compare_month_year,
    raise_date_is_not_spported,
    add_months_to_month_year,
)
from ..utils.ui import create_warning


def scrape_quotes(non_fulfilled_scraping_request):
    driver = None
    quotes = []

    try:
        pick_up_office_name = non_fulfilled_scraping_request["pick_up_office_name"]
        pick_up_office_address = non_fulfilled_scraping_request[
            "pick_up_office_address"
        ]
        drop_off_office_name = non_fulfilled_scraping_request["drop_off_office_name"]
        drop_off_office_address = non_fulfilled_scraping_request[
            "drop_off_office_address"
        ]
        pick_up_date_value = non_fulfilled_scraping_request["pick_up_date_value"]
        pick_up_time_value = non_fulfilled_scraping_request["pick_up_time_value"]
        drop_off_date_value = non_fulfilled_scraping_request["drop_off_date_value"]
        drop_off_time_value = non_fulfilled_scraping_request["drop_off_time_value"]

        chrome_options = Options()
        if constants.IS_CHROME_HEADLESS_ENABLED:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(constants.GORENTALS_BOOKING_PAGE_URL)

        __fill_select(driver, "locationPickerStart", pick_up_office_name)
        __fill_select(driver, "locationPickerEnd", drop_off_office_name)
        __fill_date_input(driver, "datePickerStart", "Pick-up date", pick_up_date_value)
        __fill_select(driver, "timePickerStart", pick_up_time_value)
        __fill_date_input(driver, "datePickerEnd", "Drop-off date", drop_off_date_value)
        __fill_select(driver, "timePickerEnd", drop_off_time_value)

        # Click the Find my car button
        find_my_car_button = wait_element_until_visible_by_xpath(
            driver, constants.SCRAPE_TIMEOUT, "//button[span='Find my car']"
        )
        find_my_car_button.click()

        try:
            wait_elements_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                "main > content > section > content > div article",
            )
        except TimeoutException as exception:
            warning = create_warning(
                "\nNo quotes were found for the non-fulfilled scraping request:\n{}".format(
                    pprint.pformat(non_fulfilled_scraping_request)
                )
            )
            print(warning)
        else:
            quotes = __scrape_quotes_on_page(driver)
    finally:
        if driver:
            driver.quit()

    return quotes


def __fill_select(driver, select_id, selected_option_text):
    selected_option_xpath = (
        "//label[@for='{}']//ul/li//span[normalize-space(text())='{}']".format(
            select_id, selected_option_text
        )
    )
    selected_option = wait_element_until_present_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        selected_option_xpath,
    )

    select_xpath = "//label[@for='{}']/div[contains(@class, '{}')]".format(
        select_id, "multiselect"
    )
    select = wait_element_until_visible_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        select_xpath,
    )

    select.click()
    selected_option.click()


def __fill_date_input(driver, date_input_id, date_picker_name, date_value):
    def calculate_month_year_difference(driver, target_month_year):
        """Calculate the difference required to decide whether to adjust the date picker."""
        current_month_year_label_xpath = "//div[@name='{}' and contains(@class, 'goDatePicker')]//div[@class='c-title']".format(
            date_picker_name
        )
        current_month_year_label = wait_element_until_visible_by_xpath(
            driver,
            constants.SCRAPE_TIMEOUT,
            current_month_year_label_xpath,
        )
        current_month_year = parse_month_year_text(current_month_year_label.text)
        difference = compare_month_year(target_month_year, current_month_year)
        return difference

    class target_month_year_to_be_visible:
        def __init__(self, target_month_year):
            self.target_month_year = target_month_year

        def __call__(self, driver):
            return calculate_month_year_difference(driver, self.target_month_year) == 0

    def wait_for_target_month_year_to_show(target_month_year):
        # Wait for target month year, or an stale element exception occurs.
        WebDriverWait(driver, constants.SCRAPE_TIMEOUT).until(
            target_month_year_to_be_visible(target_month_year)
        )

    # Open the date picker.
    date_input_css_selector = "#{}".format(date_input_id)
    date_input = wait_element_until_visible_by_css_selector(
        driver, constants.SCRAPE_TIMEOUT, date_input_css_selector
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
        prev_link_xpath = "(//div[@name='{}' and contains(@class, 'goDatePicker')]//*[name()='svg'])[1]".format(
            date_picker_name
        )
        while prev_counter <= step_count:
            prev_link = wait_element_until_visible_by_xpath(
                driver,
                constants.SCRAPE_TIMEOUT,
                prev_link_xpath,
            )
            is_prev_link_disabled = check_if_element_has_class(prev_link, "c-disabled")
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
        next_link_xpath = "(//div[@name='{}' and contains(@class, 'goDatePicker')]//*[name()='svg'])[2]".format(
            date_picker_name
        )
        while next_counter <= step_count:
            next_link = wait_element_until_visible_by_xpath(
                driver,
                constants.SCRAPE_TIMEOUT,
                next_link_xpath,
            )
            is_next_link_disabled = check_if_element_has_class(next_link, "c-disabled")
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
    day_link_xpath = "//div[@name='{}' and contains(@class, 'c-weeks-rows')]//div[normalize-space(text())='{}']".format(
        date_picker_name, day_text
    )
    day_link = wait_element_until_visible_by_xpath(
        driver, constants.SCRAPE_TIMEOUT, day_link_xpath
    )
    day_link_wrapper = day_link.find_element(By.XPATH, "..")
    day_link_wrapper_style = day_link_wrapper.get_attribute("style")
    if "opacity" in day_link_wrapper_style:
        raise_date_is_not_spported(date_value)
    day_link.click()


def __scrape_quotes_on_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    vehicle_category_sections = soup.select("main > content > section > content > div")
    quotes = []
    for vehicle_category_section in vehicle_category_sections:
        vehicle_category_name_in_company = str(vehicle_category_section.h2.string)
        quote_articles = vehicle_category_section.select("article")
        for quote_article in quote_articles:
            vehicle_category_description = str(quote_article.header.h2.string)
            vehicle_age_description = str(quote_article.header.p.string)
            price_span = quote_article.select_one(
                "content > ul > li:nth-child(2) > span:nth-child(1)"
            )
            price_text = str(price_span.string)
            price = extract_price(price_text)
            quotes.append(
                {
                    "vehicle_category_name_in_company": vehicle_category_name_in_company,
                    "vehicle_category_description": vehicle_category_description,
                    "vehicle_age_description": vehicle_age_description,
                    "price": price,
                }
            )
    return quotes
