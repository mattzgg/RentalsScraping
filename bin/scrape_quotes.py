import import_lib, time, signal, sys

from datetime import datetime
from progress.bar import ChargingBar
from lib.utils import constants
from lib.utils.web_scraping import time_until_end_of_day
from lib.utils.ui import create_info, print_exception
from lib.db.quote import (
    get_scraping_request_statistics,
    get_non_fulfilled_scraping_requests,
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


def format_today():
    return datetime.today().strftime("%d/%m/%Y")


def raise_scraping_date_passed_exception(scraping_date_str):
    scraping_request_statistics = get_scraping_request_statistics(scraping_date_str)
    total_count = scraping_request_statistics["total_count"]
    fulfilled_count = scraping_request_statistics["fulfilled_count"]
    non_fulfilled_count = total_count - fulfilled_count
    raise RuntimeError(
        "The scraping date {} passed, scraping for it has been interrupted."
        + "{} non-fulfilled scraping requests have been skipped".format(
            scraping_date_str, non_fulfilled_count
        )
    )


def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            scraping_date_str = format_today()
            scraping_request_statistics = get_scraping_request_statistics(
                scraping_date_str
            )
            total_count = scraping_request_statistics["total_count"]
            fulfilled_count = scraping_request_statistics["fulfilled_count"]
            if fulfilled_count == total_count:
                print(
                    create_info(
                        "All of today's scraping requests have been executed. "
                        + "I am going to sleep until midnight."
                    )
                )
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
                    non_fulfilled_scraping_requests = (
                        get_non_fulfilled_scraping_requests(
                            scraping_date_str, 0, constants.SQL_SELECT_LIMIT_ROW_COUNT
                        )
                    )

                    # There is no more non-fulfilled scraping requests.
                    if len(non_fulfilled_scraping_requests) == 0:
                        progress_bar.finish()
                        break

                    for (
                        non_fulfilled_scraping_request
                    ) in non_fulfilled_scraping_requests:
                        company_id = non_fulfilled_scraping_request["company_id"]
                        scrape_quotes_func = SCRAPE_QUOTES_FUNCS[company_id]
                        quotes = scrape_quotes_func(non_fulfilled_scraping_request)

                        while True:
                            is_added = quote_cache.add_quotes(
                                non_fulfilled_scraping_request, quotes
                            )
                            if not is_added:
                                # Flush then add again.
                                quote_cache.flush()
                            else:
                                break

                        progress_bar.next()
                finally:
                    quote_cache.flush()

                    current_date_str = format_today()
                    if current_date_str != scraping_date_str:
                        raise_scraping_date_passed_exception(scraping_date_str)
        except SystemExit:
            break
        except:
            print_exception()


if __name__ == "__main__":
    main()
