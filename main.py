from thrifty.location import scrape_locations as scrape_locations_for_thrifty
from thrifty.quote import scrape_quotes as scrape_quotes_for_thrifty

from budget.location import scrape_locations as scrape_locations_for_budget
from budget.quote import scrape_quotes as scrape_quotes_for_budget

from gorentals.location import (
    scrape_locations as scrape_locations_for_gorentals,
)
from gorentals.quote import scrape_quotes as scrape_quotes_for_gorentals

from db.location import save_locations
from db.quote import (
    add_todays_quote_scraping_task,
    get_todays_booking_request_statistics,
    get_todays_pending_booking_requests,
)

from utils.ui import (
    is_quit_command,
    create_option,
    create_warning,
)


def scrape_locations(*args):
    company_id = args[0]
    scrape_locations_func = SCRAPE_LOCATIONS_FUNCS[company_id]
    locations = scrape_locations_func()
    save_locations(int(company_id), locations)


def scrape_todays_rental_quotes(*args):
    task_id = add_todays_quote_scraping_task()
    print("Today's quote scraping task[", task_id, "] has been created successfully.")

    while True:
        statistics = get_todays_booking_request_statistics()
        print("Statistics: ", statistics)
        if statistics["pending_count"] == 0:
            break

        pending_booking_requests = get_todays_pending_booking_requests()
        for pending_booking_request in pending_booking_requests:
            company_id = pending_booking_request["company_id"]
            scrape_quotes_func = SCRAPE_QUOTES_FUNCS[str(company_id)]
            scrape_quotes_func(pending_booking_request)


COMMANDS = {
    "1": scrape_locations,
    "2": scrape_todays_rental_quotes,
}

SCRAPE_LOCATIONS_FUNCS = {
    "1": scrape_locations_for_thrifty,
    "2": scrape_locations_for_budget,
    "3": scrape_locations_for_gorentals,
}

SCRAPE_QUOTES_FUNCS = {
    "1": scrape_quotes_for_thrifty,
    "2": scrape_quotes_for_budget,
    "3": scrape_quotes_for_gorentals,
}


def execute_command(command):
    item_count = len(command)
    command_id = command[0]
    command_args = [] if item_count == 1 else command[1:item_count]
    command_func = COMMANDS[command_id]
    command_func(*command_args)


def prompt_locations_scraping():
    print("The following companies provide rental locations:")
    print(create_option("[1] Thrifty"))
    print(create_option("[2] Budget"))
    print(create_option("[3] GO Rentals"))
    choice = input("Please input the company ID: ")
    if is_quit_command(choice):
        return
    elif choice in (
        "1",
        "2",
        "3",
    ):
        execute_command(["1", choice])
        return


while True:
    print("Welcome to RentalsScraping!")
    print("Anytime you want to quit the current operation, please input 'q'.")
    print(create_option("[1] Scrape rental locations"))
    print(create_option("[2] Scrape today's rental quotes"))
    choice = input("Please input the command ID: ")
    if choice == "q":
        break
    elif choice == "1":
        prompt_locations_scraping()
    elif choice == "2":
        execute_command(["2"])
