from .common import execute_query


def add_offices(
    db_connection_parameters,
    company_id,
    offices=[],
    is_refresh_rental_routes_required=False,
):
    def invoke_cursor_func(cursor):
        for office in offices:
            name = office["name"]
            address = office["address"]
            args = [company_id, name, address]
            cursor.callproc("add_office", args)

    execute_query(db_connection_parameters, invoke_cursor_func)

    if is_refresh_rental_routes_required:
        refresh_rental_routes(db_connection_parameters)


def refresh_rental_routes(db_connection_parameters):
    def invoke_cursor_func(cursor):
        cursor.callproc("refresh_rental_routes")

    execute_query(db_connection_parameters, invoke_cursor_func)