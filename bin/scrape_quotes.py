import import_lib, time, signal, sys

from datetime import datetime
from progress.bar import ChargingBar
from lib.utils import constants
from lib.utils.web_scraping import time_until_end_of_day
from lib.utils.ui import create_info, print_exception
from lib.db.quote import (
    get_booking_request_statistics,
    get_non_fulfilled_booking_requests,
    QuoteCache,
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


def signal_handler(sig, frame):
    print(create_info("\nYou pressed Ctrl+C. Bye!"))
    sys.exit(0)


def __wait_until_tomorrow():
    time_until_today = time_until_end_of_day()
    time.sleep(time_until_today)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            scraping_date_str = datetime.today().strftime("%d/%m/%Y")
            booking_request_statistics = get_booking_request_statistics(
                scraping_date_str
            )
            total_count = booking_request_statistics["total_count"]
            fulfilled_count = booking_request_statistics["fulfilled_count"]
            if fulfilled_count == total_count:
                __wait_until_tomorrow()
                continue

            progress_bar = ChargingBar(
                "Scraping quotes on {}".format(scraping_date_str),
                max=total_count,
                color="green",
                suffix="%(percent)d%%, %(index)d/%(max)d, %(elapsed_td)s",
            )
            progress_bar.goto(fulfilled_count)

            quote_cache = QuoteCache()
            while True:
                try:
                    non_fulfilled_booking_requests = get_non_fulfilled_booking_requests(
                        scraping_date_str, 0, constants.SQL_SELECT_LIMIT_ROW_COUNT
                    )

                    # There is no more non-fulfilled booking requests.
                    if len(non_fulfilled_booking_requests) == 0:
                        progress_bar.finish()
                        break

                    for non_fulfilled_booking_request in non_fulfilled_booking_requests:
                        company_id = non_fulfilled_booking_request["company_id"]
                        scrape_quotes_func = SCRAPE_QUOTES_FUNCS[company_id]
                        quotes = scrape_quotes_func(non_fulfilled_booking_request)

                        while True:
                            is_added = quote_cache.add_quotes(
                                non_fulfilled_booking_request, quotes
                            )
                            if not is_added:
                                # Flush then add again.
                                quote_cache.flush()
                            else:
                                break

                        progress_bar.next()
                finally:
                    quote_cache.flush()
        except SystemExit:
            break
        except:
            print_exception()


if __name__ == "__main__":
    main()
