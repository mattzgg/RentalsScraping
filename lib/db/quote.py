from datetime import datetime
from .common import execute_query, execute_transaction
from ..utils.datatype import convert_tuple_to_dict
from ..utils.ui import create_info


def get_scraping_request_statistics(scraping_date_str):
    def invoke_cursor_func(cursor):
        args = [scraping_date_str, 0, 0]
        result_args = cursor.callproc("get_scraping_request_statistics", args)
        return {"total_count": result_args[1], "fulfilled_count": result_args[2]}

    return execute_query(invoke_cursor_func)


def get_non_fulfilled_scraping_requests(scraping_date_str, offset, row_count):
    non_fulfilled_scraping_request_property_names = [
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

    def convert_func(non_fulfilled_scraping_request):
        return convert_tuple_to_dict(
            non_fulfilled_scraping_request,
            non_fulfilled_scraping_request_property_names,
        )

    def invoke_cursor_func(cursor):
        non_fulfilled_scraping_requests = []
        cursor.callproc(
            "get_non_fulfilled_scraping_requests",
            [scraping_date_str, offset, row_count],
        )
        for result in cursor.stored_results():
            non_fulfilled_scraping_requests = list(map(convert_func, result.fetchall()))

        return non_fulfilled_scraping_requests

    return execute_query(invoke_cursor_func)


def save_quotes(non_fulfilled_scraping_request, quotes):
    def invoke_cursor_func(cursor):
        company_id = non_fulfilled_scraping_request["company_id"]
        rental_route_id = non_fulfilled_scraping_request["rental_route_id"]
        pick_up_date_id = non_fulfilled_scraping_request["pick_up_date_id"]
        pick_up_time_id = non_fulfilled_scraping_request["pick_up_time_id"]
        rental_duration_id = non_fulfilled_scraping_request["rental_duration_id"]
        created_on = datetime.now()

        query_parameters_list = []
        for quote in quotes:
            vehicle_category_name_in_company = quote["vehicle_category_name_in_company"]
            vehicle_category_description = quote["vehicle_category_description"]
            vehicle_age_description = quote["vehicle_age_description"]
            price = quote["price"]
            query_parameters_list.append(
                (
                    company_id,
                    rental_route_id,
                    pick_up_date_id,
                    pick_up_time_id,
                    rental_duration_id,
                    company_id,
                    vehicle_category_name_in_company,
                    vehicle_category_description,
                    vehicle_age_description,
                    price,
                    created_on,
                )
            )

        if query_parameters_list:
            query = """insert into rental_quote(company_id, rental_route_id,
                pick_up_date_id, pick_up_time_id, rental_duration_id,
                vehicle_category_id, price, created_on) values
                (%s, %s, %s, %s, %s, get_vehicle_category_id(%s, %s, %s, %s), %s, %s)"""
            cursor.executemany(query, query_parameters_list)

    execute_transaction(invoke_cursor_func)


class QuoteCache:
    """A simple tool to boost performance for saving quotes to database.
    There are two kinds of quotes. One is for real quotes. Real quotes has
    vehicle category id and price. The other is for scraping request fulfillment (BRF).
    Quotes which reprsent scraping request fulfilment They don't have vehicle
    category id and price.
    """

    def __init__(self):
        QuoteCache.CAPACITY = 1000
        self._cache = []
        # SQL statement used to insert a real quote
        self._query_for_real_quote = """insert into rental_quote(company_id, rental_route_id,
            pick_up_date_id, pick_up_time_id, rental_duration_id,
            vehicle_category_id, price, created_on) values
            (%s, %s, %s, %s, %s, get_vehicle_category_id(%s, %s, %s, %s), %s, %s)"""
        # SQL statement used to insert a BRF quote
        self._query_for_brf_quote = """insert into rental_quote(company_id,
            rental_route_id, pick_up_date_id, pick_up_time_id, rental_duration_id, created_on)
            values(%s, %s, %s, %s, %s, %s)"""

    def get_count(self):
        return len(self._cache)

    def add_quotes(self, non_fulfilled_scraping_request, quotes):
        # If quotes is an empty list, then a BRF quote is required.
        quotes_count = len(quotes) if len(quotes) > 0 else 1
        if quotes_count > QuoteCache.CAPACITY:
            raise Exception(
                "Quote cache is not big enough to accommodate {} quotes.".format(
                    QuoteCache.CAPACITY
                )
            )
        if self.get_count() + quotes_count > QuoteCache.CAPACITY:
            return False

        company_id = non_fulfilled_scraping_request["company_id"]
        rental_route_id = non_fulfilled_scraping_request["rental_route_id"]
        pick_up_date_id = non_fulfilled_scraping_request["pick_up_date_id"]
        pick_up_time_id = non_fulfilled_scraping_request["pick_up_time_id"]
        rental_duration_id = non_fulfilled_scraping_request["rental_duration_id"]
        created_on = datetime.now()

        if quotes:
            for quote in quotes:
                vehicle_category_name_in_company = quote[
                    "vehicle_category_name_in_company"
                ]
                vehicle_category_description = quote["vehicle_category_description"]
                vehicle_age_description = quote["vehicle_age_description"]
                price = quote["price"]
                self._cache.append(
                    (
                        company_id,
                        rental_route_id,
                        pick_up_date_id,
                        pick_up_time_id,
                        rental_duration_id,
                        company_id,
                        vehicle_category_name_in_company,
                        vehicle_category_description,
                        vehicle_age_description,
                        price,
                        created_on,
                    )
                )
        else:
            self._cache.append(
                (
                    company_id,
                    rental_route_id,
                    pick_up_date_id,
                    pick_up_time_id,
                    rental_duration_id,
                    created_on,
                )
            )

        return True

    def flush(self):
        """Save the quotes in cache to the database then empty the cache."""

        def filter_real_quotes(quote):
            return len(quote) == 11

        def filter_brf_quotes(quote):
            return len(quote) == 6

        def invoke_cursor_func(cursor):
            if self.get_count() > 0:
                _cache_for_real_quote = list(filter(filter_real_quotes, self._cache))
                if _cache_for_real_quote:
                    cursor.executemany(
                        self._query_for_real_quote, _cache_for_real_quote
                    )

                _cache_for_brf_quote = list(filter(filter_brf_quotes, self._cache))
                if _cache_for_brf_quote:
                    cursor.executemany(self._query_for_brf_quote, _cache_for_brf_quote)

                info = create_info(
                    "\n{} quotes have been saved to the database.".format(
                        self.get_count()
                    )
                )
                print(info)

        try:
            execute_transaction(invoke_cursor_func)
        finally:
            self._cache = []
