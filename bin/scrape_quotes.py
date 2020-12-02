#!/usr/bin/env python3
import import_lib
import time
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from progress.bar import ChargingBar
from multiprocessing import Pool, cpu_count

from lib.utils import constants
from lib.utils.web_scraping import time_until_end_of_day
from lib.utils.ui import create_info, print_exception
from lib.utils.db_config import (
    get_db_config_file_name_help,
    get_db_connection_parameters,
)
from lib.utils.scrape_quotes_pool import sqp_initializer, sqp_worker
from lib.db.quote import (
    get_scraping_request_statistics,
    get_pending_scraping_requests,
    QuoteCache,
)


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "db_config_file_name",
        help=get_db_config_file_name_help(),
    )
    parser.add_argument(
        "--wait-element-timeout",
        type=int,
        default=10,
        help="The timeout used by the Selenium explicit waits, defaults to %(default)s seconds",
    )
    parser.add_argument(
        "--dom-ready-timeout",
        type=int,
        default=10,
        help="The timeout used to wait until the document.readyState becomes complete, defaults to %(default)s seconds, ",
    )
    parser.add_argument(
        "--pool-size",
        type=int,
        default=cpu_count(),
        help="The number of processes that the pool creates to scrape quotes in parallel, defaults to %(default)s",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="The number of pending scraping requests retrieved from the database at a time, defaults to %(default)s",
    )
    parser.add_argument(
        "--cache-capacity",
        type=int,
        default=1000,
        help="The maximun number of rental quotes that the cache can accommodate, defaults to %(default)s",
    )
    parser.add_argument(
        "--headless", action="store_true", help="Enable to use headless Chrome"
    )
    args = parser.parse_args()

    db_connection_parameters = get_db_connection_parameters(args.db_config_file_name)

    return {
        "db_connection_parameters": db_connection_parameters,
        "scraping_config": {
            "wait_element_timeout": args.wait_element_timeout,
            "dom_ready_timeout": args.dom_ready_timeout,
            "headless": args.headless,
        },
        "pool_size": args.pool_size,
        "batch_size": args.batch_size,
        "cache_config": {
            "db_connection_parameters": db_connection_parameters,
            "capacity": args.cache_capacity,
        },
    }


def create_driver(scraping_config):
    options = Options()
    if scraping_config["headless"]:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def __wait_until_tomorrow():
    time_until_today = time_until_end_of_day()
    time.sleep(time_until_today)


def format_today():
    return datetime.today().strftime("%d/%m/%Y")


def raise_scraping_date_passed_exception(db_connection_parameters, scraping_date_str):
    scraping_request_statistics = get_scraping_request_statistics(
        db_connection_parameters, scraping_date_str
    )
    total_count = scraping_request_statistics["total_count"]
    processed_count = scraping_request_statistics["processed_count"]
    pending_count = total_count - processed_count
    raise RuntimeError(
        (
            "The scraping date {} passed, scraping for it has been interrupted."
            + "{} pending scraping requests have been skipped"
        ).format(scraping_date_str, pending_count)
    )


def main():
    args = parse_args()
    db_connection_parameters = args["db_connection_parameters"]

    while True:
        try:
            scraping_date_str = format_today()
            scraping_request_statistics = get_scraping_request_statistics(
                db_connection_parameters, scraping_date_str
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
            quote_cache = QuoteCache(args["cache_config"])

            with Pool(
                processes=args["pool_size"],
                initializer=sqp_initializer,
                initargs=(
                    create_driver,
                    args["scraping_config"],
                ),
            ) as pool:
                while True:
                    try:
                        pending_scraping_requests = get_pending_scraping_requests(
                            db_connection_parameters,
                            scraping_date_str,
                            0,
                            args["batch_size"],
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
                            raise_scraping_date_passed_exception(
                                db_connection_parameters, scraping_date_str
                            )
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
