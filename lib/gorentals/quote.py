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
    click_element,
    extract_price,
)
from ..utils.ui import create_warning


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
        pick_up_date_value = non_fulfilled_booking_request[
            "pick_up_date_value"
        ]  # 06/11/2020
        pick_up_time_value = non_fulfilled_booking_request[
            "pick_up_time_value"
        ]  # 09:00 AM
        drop_off_date_value = non_fulfilled_booking_request["drop_off_date_value"]
        drop_off_time_value = non_fulfilled_booking_request["drop_off_time_value"]

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
        click_element(driver, find_my_car_button)
        try:
            wait_elements_until_visible_by_css_selector(
                driver,
                constants.SCRAPE_TIMEOUT,
                "main > content > section > content > div article",
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

    select_caret_xpath = "//label[@for='{}']//div[@class='{}']".format(
        select_id, "multiselect__select"
    )
    select_caret = wait_element_until_visible_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        select_caret_xpath,
    )

    click_element(driver, select_caret)
    click_element(driver, selected_option)


def __fill_date_input(driver, date_input_id, date_picker_name, date_value):
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
    click_element(driver, date_input)

    current_date = parse_date_text(date_value)

    # Calculate the parameters required to decide whether to adjust the date picker.
    month_year_label_xpath = "//div[@name='{}' and contains(@class, 'goDatePicker')]//div[@class='c-title']".format(
        date_picker_name
    )
    month_year_label = wait_element_until_visible_by_xpath(
        driver,
        constants.SCRAPE_TIMEOUT,
        month_year_label_xpath,
    )
    month_year = parse_month_year_text(month_year_label.text)
    current_month_year = {
        "month": current_date["month"],
        "year": current_date["year"],
    }
    difference = compare_month_year(current_month_year, month_year)

    # Adjust the date picker to make it display proper dates which include the current date.
    if difference < 0:
        prev_counter = 0
        step_count = abs(difference)
        prev_link_xpath = "(//div[@name='{}' and contains(@class, 'goDatePicker')]//*[name()='svg'])[1]".format(
            date_picker_name
        )
        while prev_counter < step_count:
            prev_link = wait_element_until_visible_by_xpath(
                driver,
                constants.SCRAPE_TIMEOUT,
                prev_link_xpath,
            )
            is_prev_link_disabled = check_if_element_has_class(prev_link, "c-disabled")
            if is_prev_link_disabled:
                raise_date_is_not_spported()
            click_element(driver, prev_link)
            prev_counter += 1
    elif difference > 0:
        next_counter = 0
        step_count = difference
        next_link_xpath = "(//div[@name='{}' and contains(@class, 'goDatePicker')]//*[name()='svg'])[2]".format(
            date_picker_name
        )
        while next_counter < step_count:
            next_link = wait_element_until_visible_by_xpath(
                driver,
                constants.SCRAPE_TIMEOUT,
                next_link_xpath,
            )
            is_next_link_disabled = check_if_element_has_class(next_link, "c-disabled")
            if is_next_link_disabled:
                raise_date_is_not_spported()
            click_element(driver, next_link)
            next_counter += 1

    # Select the current date
    day_text = str(current_date["day"])
    day_link_xpath = "//div[@name='{}' and contains(@class, 'c-weeks-rows')]//div[normalize-space(text())='{}']".format(
        date_picker_name, day_text
    )
    day_link = wait_element_until_visible_by_xpath(
        driver, constants.SCRAPE_TIMEOUT, day_link_xpath
    )
    day_link_wrapper = day_link.find_element(By.XPATH, "..")
    day_link_wrapper_style = day_link_wrapper.get_attribute("style")
    if "opacity" in day_link_wrapper_style:
        raise_date_is_not_spported()
    click_element(driver, day_link)


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
            quote_span = quote_article.select(
                "content > ul > li:nth-child(2) > span:nth-child(1)"
            )[0]
            quote_text = str(quote_span.string)
            price = extract_price(quote_text)
            quotes.append(
                {
                    "vehicle_category_name_in_company": vehicle_category_name_in_company,
                    "vehicle_category_description": vehicle_category_description,
                    "vehicle_age_description": vehicle_age_description,
                    "price": price,
                }
            )
    return quotes
