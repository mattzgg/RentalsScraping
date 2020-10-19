import datetime

from db.common import execute_query, execute_transaction
from utils.datatype import convert_tuple_to_dict


def add_todays_quote_scraping_task():
    def invoke_cursor_func(cursor):
        args = [0]
        result_args = cursor.callproc("add_todays_quote_scraping_task", args)
        return result_args[0]

    return execute_query(invoke_cursor_func)


def get_pending_booking_requests():
    def invoke_cursor_func(cursor):
        starting_index = 0
        page_count = 1000
        total = 0
        while True:
            pending_booking_requests = []
            args = [starting_index, page_count]
            cursor.callproc("get_pending_booking_requests", args)
            for result in cursor.stored_results():
                pending_booking_requests = result.fetchall()
                total += len(pending_booking_requests)
                for pending_booking_request in pending_booking_requests:
                    print(pending_booking_request)

            if len(pending_booking_requests) == 0:
                break

            starting_index += page_count

        print("The total of today's pending booking requests is ", str(total))

    execute_query(invoke_cursor_func)


def save_vehicle_categroy(vehicle_category):
    pass


def save_vehicle_model(vehicle_model):
    pass


def save_rental_quote(rental_quote):
    pass
