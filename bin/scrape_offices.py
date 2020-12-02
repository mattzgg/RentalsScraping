import import_lib
import argparse
from lib.thrifty.location import scrape_offices as scrape_offices_from_thrifty
from lib.budget.location import scrape_offices as scrape_offices_from_budget
from lib.gorentals.location import scrape_offices as scrape_offices_from_gorentals
from lib.db.location import add_offices, refresh_rental_routes
from lib.utils import constants
from lib.utils.db_config import (
    get_db_config_file_name_help,
    get_db_connection_parameters,
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
        help="The timeout used to wait until the document.readyState becomes complete, defaults to %(default)s seconds",
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
    }


def main():
    args = parse_args()
    db_connection_parameters = args["db_connection_parameters"]
    scraping_config = args["scraping_config"]

    print("Start to handle Thrifty's offices.")
    thrifty_offices = scrape_offices_from_thrifty(scraping_config)
    add_offices(constants.THRIFTY_COMPANY_ID, thrifty_offices)
    print("Thrifty's offices have been fetched and stored successfully.")

    print("Start to handle Budget's offices.")
    budget_offices = scrape_offices_from_budget(scraping_config)
    add_offices(constants.BUDGET_COMPANY_ID, budget_offices)
    print("Budget's offices have been fetched and stored successfully.")

    print("Start to handle GO Rentals's offices.")
    gorentals_offices = scrape_offices_from_gorentals(scraping_config)
    add_offices(constants.GORENTALS_COMPANY_ID, gorentals_offices)
    print("GO Rentals's offices have been fetched and stored successfully.")

    print("Start to refresh rental routes.")
    refresh_rental_routes(db_connection_parameters)
    print("Rental routes have been refreshed successfully.")


if __name__ == "__main__":
    main()
