import logging
from .common import execute_transaction


def add_offices(
    db_connection_parameters,
    company_id,
    offices=[],
    is_refresh_rental_routes_required=False,
):
    logger = logging.getLogger(__name__)

    def invoke_cursor_func(cursor):
        for office in offices:
            name = office["name"]
            address = office["address"]
            args = [company_id, name, address]
            cursor.callproc("add_office", args)

    offices_count = len(offices)
    logger.info(f"It starts to save {offices_count} offices to the database.")
    execute_transaction(db_connection_parameters, invoke_cursor_func)
    logger.info(f"{offices_count} offices have been saved to the database.")

    if is_refresh_rental_routes_required:
        refresh_rental_routes(db_connection_parameters)


def refresh_rental_routes(db_connection_parameters):
    logger = logging.getLogger(__name__)

    def invoke_cursor_func(cursor):
        cursor.callproc("refresh_rental_routes")

    logger.info("It starts to refresh the rental routes.")
    execute_transaction(db_connection_parameters, invoke_cursor_func)
    logger.info("Rental routes have been refreshed.")
