import datetime

from db.common import execute_query, execute_transaction
from utils.datatype import convert_tuple_to_dict


def add_todays_quote_scraping_task():
    def invoke_cursor_func(cursor):
        args = [0]
        result_args = cursor.callproc("add_todays_quote_scraping_task", args)
        return result_args[0]

    return execute_query(invoke_cursor_func)


def get_todays_booking_request_statistics():
    def invoke_cursor_func(cursor):
        args = [0, 0]
        result_args = cursor.callproc("get_todays_booking_request_statistics", args)
        return {"total": result_args[0], "pending_count": result_args[1]}

    return execute_query(invoke_cursor_func)


def get_todays_pending_booking_requests():
    pending_booking_request_property_names = [
        "company_id",
        "booking_request_id",
        "rental_route_id",
        "pick_up_location_name",
        "drop_off_location_name",
        "pick_up_location_input_value",
        "drop_off_location_input_value",
        "pick_up_date",
        "pick_up_time",
        "drop_off_date",
        "drop_off_time",
    ]

    def convert_func(pending_booking_request):
        return convert_tuple_to_dict(
            pending_booking_request, pending_booking_request_property_names
        )

    def invoke_cursor_func(cursor):
        pending_booking_requests = []

        cursor.callproc("get_todays_pending_booking_requests", [0, 1000])
        for result in cursor.stored_results():
            pending_booking_requests = map(convert_func, result.fetchall())

        return pending_booking_requests

    return execute_query(invoke_cursor_func)


def save_vehicle_categroy(vehicle_category):
    pass


def save_vehicle_model(vehicle_model):
    pass


def save_rental_quote(rental_quote):
    pass
