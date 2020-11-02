from .common import execute_query


def add_offices(company_id, offices=[], is_refresh_rental_routes_required=False):
    def invoke_cursor_func(cursor):
        for office in offices:
            name = office["name"]
            address = office["address"]
            args = [company_id, name, address]
            cursor.callproc("add_office", args)

    execute_query(invoke_cursor_func)

    if is_refresh_rental_routes_required:
        refresh_rental_routes()


def refresh_rental_routes():
    def invoke_cursor_func(cursor):
        cursor.callproc("refresh_rental_routes")

    execute_query(invoke_cursor_func)