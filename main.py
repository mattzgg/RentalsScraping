from termcolor import colored
from thrifty.location import scrape_locations as scrape_locations_for_thrifty
from budget.location import scrape_locations as scrape_locations_for_budget
from gorentals.location import (
    scrape_locations as scrape_locations_for_gorentals,
)
from db.location import save_scraped_locations


def load_or_refresh_locations(*args):
    company_id = args[0]
    scape_location_func = SCRAPE_LOCATION_FUNCS[company_id]
    scraped_location_names = scape_location_func()
    save_scraped_locations(int(company_id), scraped_location_names)


def scrape_quotes(*args):
    pass


COMMAND_FUNCS = {
    "1": load_or_refresh_locations,
    "2": scrape_quotes,
}

SCRAPE_LOCATION_FUNCS = {
    "1": scrape_locations_for_thrifty,
    "2": scrape_locations_for_budget,
    "3": scrape_locations_for_gorentals,
}


def execute_command(command):
    command_id = command[0]
    command_args = command[1 : len(command)]
    command_func = COMMAND_FUNCS[command_id]
    command_func(*command_args)


def prompt_load_or_refresh_locations():
    while True:
        print("The locations can be loaded or refreshed from the following companies:")
        print(colored("    [1] Thrifty", "green"))
        print(colored("    [2] Budget", "green"))
        print(colored("    [3] GORentals", "green"))
        choice = input(
            "Please input the company ID[1, 2, 3], or 'q' to go back to the main menu: "
        )
        if choice == "q":
            break
        elif choice == "1":
            execute_command(["1", "1"])
            break
        elif choice == "2":
            execute_command(["1", "2"])
            break
        elif choice == "3":
            execute_command(["1", "3"])
            break


while True:
    print("Welcome to RentalsScraping!")
    print(colored("    [1] Load / Refresh locations", "green"))
    print(colored("    [2] Scrap the quotes", "green"))
    choice = input("Please input the command ID[1, 2], or 'q' to quite: ")
    if choice == "q":
        break
    elif choice == "1":
        prompt_load_or_refresh_locations()
