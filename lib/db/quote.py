from .common import execute_query
from ..utils.datatype import convert_tuple_to_dict


def get_booking_request_statistics(scraping_date_str):
    def invoke_cursor_func(cursor):
        args = [scraping_date_str, 0, 0]
        result_args = cursor.callproc("get_booking_request_statistics", args)
        return {"total_count": result_args[1], "fulfilled_count": result_args[2]}

    return execute_query(invoke_cursor_func)


def get_non_fulfilled_booking_requests(scraping_date_str, offset, row_count):
    non_fulfilled_booking_request_property_names = [
        "company_id",
        "rental_route_id",
        "pick_up_date_id",
        "pick_up_time_id",
        "rental_duration_id",
        "pick_up_office_name",
        "pick_up_office_address",
        "drop_off_office_name",
        "drop_off_office_address",
        "pick_up_date_value",
        "pick_up_time_value",
        "drop_off_date_value",
        "drop_off_time_value",
    ]

    def convert_func(non_fulfilled_booking_request):
        return convert_tuple_to_dict(
            non_fulfilled_booking_request, non_fulfilled_booking_request_property_names
        )

    def invoke_cursor_func(cursor):
        non_fulfilled_booking_requests = []
        cursor.callproc(
            "get_non_fulfilled_booking_requests", [scraping_date_str, offset, row_count]
        )
        for result in cursor.stored_results():
            non_fulfilled_booking_requests = list(map(convert_func, result.fetchall()))

        return non_fulfilled_booking_requests

    return execute_query(invoke_cursor_func)


def save_vehicle_categroy(vehicle_category):
    pass


def save_vehicle_model(vehicle_model):
    pass


def save_rental_quote(rental_quote):
    pass
