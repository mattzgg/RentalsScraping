from thrifty.location import scrape_locations as scrape_locations_for_thrifty
from budget.location import scrape_locations as scrape_locations_for_budget
from gorentals.location import (
    scrape_locations as scrape_locations_for_gorentals,
)
from db.location import save_locations
from db.quote import (
    get_rental_duration_operations,
    create_quote_scraping_task as create_quote_scraping_task_in_db,
)
from utils.ui import (
    is_quit_command,
    is_empty_string,
    is_valid_db_entity_id,
    create_option,
    create_warning,
    parse_booking_request_template_configs_str,
)


def scrape_locations(*args):
    company_id = args[0]
    scrape_locations_func = SCRAPE_LOCATIONS_FUNCS[company_id]
    locations = scrape_locations_func()
    save_locations(int(company_id), locations)


def create_quote_scraping_task(*args):
    created_by = args[0]
    rental_duration_operation_id = args[1]
    booking_request_template_configs = args[2]

    quote_scraping_task_id = create_quote_scraping_task_in_db(
        created_by, rental_duration_operation_id, booking_request_template_configs
    )
    print(
        "The quote scraping task["
        + str(quote_scraping_task_id)
        + "] has been created successfully."
    )


def scrape_quotes(*args):
    pass


COMMANDS = {
    "1": scrape_locations,
    "2": create_quote_scraping_task,
    "3": scrape_quotes,
}

SCRAPE_LOCATIONS_FUNCS = {
    "1": scrape_locations_for_thrifty,
    "2": scrape_locations_for_budget,
    "3": scrape_locations_for_gorentals,
}


def execute_command(command):
    command_id = command[0]
    command_args = command[1 : len(command)]
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


def prompt_quote_scraping_task_creation():
    created_by = None
    rental_duration_operation_id = None
    valid_rental_duration_operation_ids = []
    booking_request_template_configs = []

    # capture the name of person who creates this task
    while is_empty_string(created_by):
        created_by = input("Please input your name: ")
        if is_quit_command(created_by):
            return
        elif is_empty_string(created_by):
            print(create_warning("Name is invalid."))

    # capture the rental duration operation ID
    while not is_valid_db_entity_id(
        rental_duration_operation_id, valid_rental_duration_operation_ids
    ):
        print("The available rental duration operations are:")
        rental_duration_operations = get_rental_duration_operations()
        valid_rental_duration_operation_ids = []
        for rental_duration_operation in rental_duration_operations:
            id = rental_duration_operation["id"]
            description = rental_duration_operation["description"]
            valid_rental_duration_operation_ids.append(id)
            print(create_option("[" + str(id) + "] " + description))

        rental_duration_operation_id = input(
            "Please input the rental duration operation ID: "
        )
        if is_quit_command(rental_duration_operation_id):
            return
        elif not is_valid_db_entity_id(
            rental_duration_operation_id, valid_rental_duration_operation_ids
        ):
            print(create_warning("Rental duration operation ID is invalid."))

    # capture booking request template configs related to the new task
    while not booking_request_template_configs:
        booking_request_template_configs_str = input(
            "Please input the booking request template configs string: "
        )
        if is_quit_command(booking_request_template_configs_str):
            return

        booking_request_template_configs = parse_booking_request_template_configs_str(
            booking_request_template_configs_str
        )
        if not booking_request_template_configs:
            print(
                create_warning(
                    "The booking request template configs string is invalid."
                )
            )

    execute_command(
        [
            "2",
            created_by,
            int(rental_duration_operation_id),
            booking_request_template_configs,
        ]
    )


def prompt_quotes_scraping():
    quote_scraping_task_id = None

    while not is_valid_db_entity_id(quote_scraping_task_id):
        quote_scraping_task_id = input("Please input the quote scraping task ID: ")
        if is_quit_command(quote_scraping_task_id):
            return
        elif not is_valid_db_entity_id(quote_scraping_task_id):
            print(create_warning("The quote scraping task ID is invalid."))

    execute_command(["3", int(quote_scraping_task_id)])


while True:
    print("Welcome to RentalsScraping!")
    print("Anytime you want to quit the current operation, please input 'q'.")
    print(create_option("[1] Scrape rental locations"))
    print(create_option("[2] Create a rental quote scraping task"))
    print(create_option("[3] Scrape rental quotes"))
    choice = input("Please input the command ID: ")
    if choice == "q":
        break
    elif choice == "1":
        prompt_locations_scraping()
    elif choice == "2":
        prompt_quote_scraping_task_creation()
    elif choice == "3":
        prompt_quotes_scraping()
