import import_lib
from lib.thrifty.location import scrape_offices as scrape_offices_from_thrifty
from lib.budget.location import scrape_offices as scrape_offices_from_budget
from lib.gorentals.location import scrape_offices as scrape_offices_from_gorentals
from lib.db.location import add_offices, refresh_rental_routes
from lib.utils import constants


def main():
    print("Start to handle Thrifty's offices.")
    thrifty_offices = scrape_offices_from_thrifty()
    add_offices(constants.THRIFTY_COMPANY_ID, thrifty_offices)
    print("Thrifty's offices have been fetched and stored successfully.")

    print("Start to handle Budget's offices.")
    budget_offices = scrape_offices_from_budget()
    add_offices(constants.BUDGET_COMPANY_ID, budget_offices)
    print("Budget's offices have been fetched and stored successfully.")

    print("Start to handle GO Rentals's offices.")
    gorentals_offices = scrape_offices_from_gorentals()
    add_offices(constants.GORENTALS_COMPANY_ID, gorentals_offices)
    print("GO Rentals's offices have been fetched and stored successfully.")

    print("Start to refresh rental routes.")
    refresh_rental_routes()
    print("Rental routes have been refreshed successfully.")


if __name__ == "__main__":
    main()
