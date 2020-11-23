import import_lib, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from progress.bar import ChargingBar
from multiprocessing import Pool

from lib.utils import constants
from lib.utils.datatype import is_list
from lib.utils.web_scraping import time_until_end_of_day
from lib.utils.ui import create_info, print_exception
from lib.db.quote import (
    get_scraping_request_statistics,
    get_pending_scraping_requests,
    QuoteCache,
)
from lib.utils.scrape_quotes_pool import sqp_initializer, sqp_worker


def create_driver():
    options = Options()
    if constants.IS_CHROME_HEADLESS_ENABLED:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def __wait_until_tomorrow():
    time_until_today = time_until_end_of_day()
    time.sleep(time_until_today)


def format_today():
    return datetime.today().strftime("%d/%m/%Y")


def raise_scraping_date_passed_exception(scraping_date_str):
    scraping_request_statistics = get_scraping_request_statistics(scraping_date_str)
    total_count = scraping_request_statistics["total_count"]
    processed_count = scraping_request_statistics["processed_count"]
    pending_count = total_count - processed_count
    raise RuntimeError(
        "The scraping date {} passed, scraping for it has been interrupted."
        + "{} pending scraping requests have been skipped".format(
            scraping_date_str, pending_count
        )
    )


def main():
    while True:
        try:
            scraping_date_str = format_today()
            scraping_request_statistics = get_scraping_request_statistics(
                scraping_date_str
            )
            total_count = scraping_request_statistics["total_count"]
            processed_count = scraping_request_statistics["processed_count"]
            if processed_count == total_count:
                print(
                    create_info(
                        "All of today's scraping requests have been executed. "
                        + "I am going to sleep until midnight."
                    )
                )
                __wait_until_tomorrow()
                continue

            # The progress bar shows how many scraping requests have been processed.
            progress_bar = ChargingBar(
                "Scraping quotes on {}".format(scraping_date_str),
                max=total_count,
                color="green",
                suffix="%(percent)d%%, %(index)d/%(max)d, %(elapsed_td)s",
            )
            progress_bar.goto(processed_count)

            # The quote cache boosts the performance of saving data to the database.
            quote_cache = QuoteCache()

            with Pool(initializer=sqp_initializer, initargs=(create_driver,)) as pool:
                while True:
                    try:
                        pending_scraping_requests = get_pending_scraping_requests(
                            scraping_date_str,
                            0,
                            constants.SQL_SELECT_LIMIT_ROW_COUNT,
                        )

                        pending_scraping_requests_count = len(pending_scraping_requests)
                        # There are no more pending scraping requests.
                        if pending_scraping_requests_count == 0:
                            progress_bar.finish()
                            pool.close()
                            pool.join()
                            break

                        for result in pool.imap(sqp_worker, pending_scraping_requests):
                            while True:
                                is_added = quote_cache.add_quotes(result)
                                if not is_added:
                                    # Flush then add again.
                                    quote_cache.flush()
                                else:
                                    break

                            progress_bar.next()
                    except:
                        pool.close()
                        pool.join()
                        raise
                    finally:
                        quote_cache.flush()

                        current_date_str = format_today()
                        if current_date_str != scraping_date_str:
                            raise_scraping_date_passed_exception(scraping_date_str)
        except (KeyboardInterrupt, SystemExit):
            print(
                create_info(
                    "\nYou have pressed Ctrl + C, the program will terminate immediately. Bye!"
                )
            )
            break
        except:
            print_exception()


if __name__ == "__main__":
    main()
