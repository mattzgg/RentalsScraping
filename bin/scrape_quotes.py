import import_lib
import time
from datetime import datetime
from progress.bar import ChargingBar
from lib.utils import constants
from lib.utils.web_scraping import time_until_end_of_day
from lib.db.quote import (
    get_booking_request_statistics,
    get_non_fulfilled_booking_requests,
)
from lib.thrifty.quote import scrape_quotes as scrape_quotes_from_thrifty
from lib.budget.quote import scrape_quotes as scrape_quotes_from_budget
from lib.gorentals.quote import scrape_quotes as scrape_quotes_from_gorentals

SCRAPE_QUOTES_FUNCS = dict(
    [
        (
            constants.THRIFTY_COMPANY_ID,
            scrape_quotes_from_thrifty,
        ),
        (
            constants.BUDGET_COMPANY_ID,
            scrape_quotes_from_budget,
        ),
        (
            constants.GORENTALS_COMPANY_ID,
            scrape_quotes_from_gorentals,
        ),
    ]
)


def wait_until_tomorrow():
    time_until_today = time_until_end_of_day()
    time.sleep(time_until_today)


def main():
    while True:
        scraping_date_str = datetime.today().strftime("%d/%m/%Y")
        booking_request_statistics = get_booking_request_statistics(scraping_date_str)
        total_count = booking_request_statistics["total_count"]
        fulfilled_count = booking_request_statistics["fulfilled_count"]
        if fulfilled_count == total_count:
            wait_until_tomorrow()
            continue

        progress_bar = ChargingBar(
            "Scraping quotes",
            max=total_count,
            color="green",
            suffix="%(percent)d%%, %(index)d/%(max)d, %(elapsed_td)s",
        )
        progress_bar.goto(fulfilled_count)
        offset = 0
        while True:
            non_fulfilled_booking_requests = get_non_fulfilled_booking_requests(
                scraping_date_str, offset, constants.SQL_SELECT_LIMIT_ROW_COUNT
            )

            # There is no more non-fulfilled booking requests.
            if len(non_fulfilled_booking_requests) == 0:
                progress_bar.finish()
                break

            for non_fulfilled_booking_request in non_fulfilled_booking_requests:
                company_id = non_fulfilled_booking_request["company_id"]
                scrape_quotes_func = SCRAPE_QUOTES_FUNCS[company_id]
                scrape_quotes_func(non_fulfilled_booking_request)
                progress_bar.next()

            offset += constants.SQL_SELECT_LIMIT_ROW_COUNT


if __name__ == "__main__":
    main()
