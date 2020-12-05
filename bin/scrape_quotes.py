#!/usr/bin/env python3
import import_lib
import time
import argparse
import logging
import signal
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER as SELENIUM_LOGGER
from datetime import datetime
from progress.bar import ChargingBar
from multiprocessing import Pool, Process, Queue, Event, cpu_count
from pathlib import Path

from lib.utils.constants import (
    THRIFTY_COMPANY_ID,
    BUDGET_COMPANY_ID,
    GORENTALS_COMPANY_ID,
    LOGGER_MAIN,
)
from lib.utils.web_scraping import time_until_end_of_day
from lib.utils.ui import create_info, print_exception
from lib.utils.db_config import (
    get_db_config_file_name_help,
    get_db_connection_parameters,
)
from lib.utils.logging_helpers import logging_listener_worker, configure_log_dispatcher
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
        "--company-ids",
        nargs="+",
        type=int,
        default=[
            THRIFTY_COMPANY_ID,
            BUDGET_COMPANY_ID,
            GORENTALS_COMPANY_ID,
        ],
        help=(
            "A list of car rental company id, defaults to %(default)s. "
            + "Thrifty: {}, Budget: {}, GO rentals: {}"
        ).format(
            THRIFTY_COMPANY_ID,
            BUDGET_COMPANY_ID,
            GORENTALS_COMPANY_ID,
        ),
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
        "company_ids": args.company_ids,
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


def __initialize_logging(log_queue, sigint_event):
    log_config_file_path = Path(Path(__file__), "../../config/logging.conf").resolve()
    logging_listener = Process(
        target=logging_listener_worker,
        args=(
            log_config_file_path,
            log_queue,
            sigint_event,
        ),
    )
    logging_listener.start()

    configure_log_dispatcher(log_queue)


def create_driver(scraping_config):
    # Selenium outputs copious debug info, so the level should be set to WARNING.
    SELENIUM_LOGGER.setLevel(logging.WARNING)
    options = Options()
    if scraping_config["headless"]:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def __wait_until_tomorrow():
    time_until_today = time_until_end_of_day()
    time.sleep(time_until_today)


def format_today():
    return datetime.today().strftime("%d/%m/%Y")


def check_if_scraping_date_passed(
    db_connection_parameters, company_ids, scraping_date_str
):
    current_date_str = format_today()
    if current_date_str != scraping_date_str:
        scraping_request_statistics_list = get_scraping_request_statistics_list(
            db_connection_parameters, company_ids, scraping_date_str
        )
        cumulative_scraping_request_statistics = (
            get_cumulative_scraping_request_statistics(scraping_request_statistics_list)
        )
        cumulative_total_count = cumulative_scraping_request_statistics["total_count"]
        cumulative_processed_count = cumulative_scraping_request_statistics[
            "processed_count"
        ]
        cumulative_pending_count = cumulative_total_count - cumulative_processed_count
        raise RuntimeError(
            (
                "The scraping date {} passed, scraping for it has been interrupted."
                + "{} pending scraping requests have been skipped"
            ).format(scraping_date_str, cumulative_pending_count)
        )


def get_scraping_request_statistics_list(
    db_connection_parameters, company_ids, scraping_date_str
):
    return list(
        map(
            lambda company_id: get_scraping_request_statistics(
                db_connection_parameters, company_id, scraping_date_str
            ),
            company_ids,
        )
    )


def get_cumulative_scraping_request_statistics(scraping_request_statistics_list):
    return {
        "total_count": sum(
            map(lambda item: item["total_count"], scraping_request_statistics_list)
        ),
        "processed_count": sum(
            map(
                lambda item: item["processed_count"],
                scraping_request_statistics_list,
            )
        ),
    }


def get_ids_of_companies_with_workload(scraping_request_statistics_list):
    return list(
        map(
            lambda item: item["company_id"],
            filter(
                lambda item: item["processed_count"] < item["total_count"],
                scraping_request_statistics_list,
            ),
        )
    )


def __handle_sigint(sig, frame):
    logger = logging.getLogger(LOGGER_MAIN)
    logger.info("Ctrl+C have been pressed, RentalsScraping is about to exit.")
    sys.exit(0)


def main():
    args = parse_args()
    db_connection_parameters = args["db_connection_parameters"]
    company_ids = args["company_ids"]

    # Register the custom SIGINT event handler
    signal.signal(signal.SIGINT, __handle_sigint)

    # This event is used to quit the logging listener process
    sigint_event = Event()

    # Initialize the logging system which supports logging in an enviroment with multiprocessing
    log_queue = Queue(-1)
    __initialize_logging(log_queue, sigint_event)
    logger = logging.getLogger(LOGGER_MAIN)
    logger.info("RentalsScraping started.")

    while True:
        try:
            scraping_date_str = format_today()
            logger.info(f"Set the scraping date to {scraping_date_str}.")
            scraping_request_statistics_list = get_scraping_request_statistics_list(
                db_connection_parameters, company_ids, scraping_date_str
            )
            logger.info(
                f"Scraping request statistics list for {company_ids} and {scraping_date_str} has been fetched."
            )
            cumulative_scraping_request_statistics = (
                get_cumulative_scraping_request_statistics(
                    scraping_request_statistics_list
                )
            )
            cumulative_total_count = cumulative_scraping_request_statistics[
                "total_count"
            ]
            cumulative_processed_count = cumulative_scraping_request_statistics[
                "processed_count"
            ]
            if cumulative_processed_count == cumulative_total_count:
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
                max=cumulative_total_count,
                color="green",
                suffix="%(percent)d%%, %(index)d/%(max)d, %(elapsed_td)s",
            )
            progress_bar.goto(cumulative_processed_count)

            ids_of_companies_with_workload = get_ids_of_companies_with_workload(
                scraping_request_statistics_list
            )

            # The quote cache boosts the performance of saving data to the database.
            quote_cache = QuoteCache(args["cache_config"])

            with Pool(
                processes=args["pool_size"],
                initializer=sqp_initializer,
                initargs=(
                    create_driver,
                    args["scraping_config"],
                    log_queue,
                ),
            ) as pool:
                try:
                    for company_id in ids_of_companies_with_workload:
                        while True:
                            try:
                                pending_scraping_requests = (
                                    get_pending_scraping_requests(
                                        db_connection_parameters,
                                        company_id,
                                        scraping_date_str,
                                        0,
                                        args["batch_size"],
                                    )
                                )

                                pending_scraping_requests_count = len(
                                    pending_scraping_requests
                                )
                                if pending_scraping_requests_count == 0:
                                    # All pending scraping requests have been processed for the company
                                    break

                                for result in pool.imap(
                                    sqp_worker, pending_scraping_requests
                                ):
                                    while True:
                                        is_added = quote_cache.add_quotes(result)
                                        if not is_added:
                                            # Flush then add again.
                                            quote_cache.flush()
                                        else:
                                            break

                                    progress_bar.next()

                                check_if_scraping_date_passed(
                                    db_connection_parameters,
                                    company_ids,
                                    scraping_date_str,
                                )
                            finally:
                                quote_cache.flush()

                    # All pending scraping requests have been processed
                    progress_bar.finish()
                finally:
                    pool.close()
                    pool.join()
        except SystemExit:
            sigint_event.set()
            break
        except:
            print_exception()


if __name__ == "__main__":
    main()
