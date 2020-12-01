import pprint
from datetime import datetime
from .common import execute_query, execute_transaction
from ..utils.datatype import convert_tuple_to_dict
from ..utils.ui import create_info


def get_scraping_request_statistics(scraping_date_str):
    def invoke_cursor_func(cursor):
        args = [scraping_date_str, 0, 0]
        result_args = cursor.callproc("get_scraping_request_statistics", args)
        return {"total_count": result_args[1], "processed_count": result_args[2]}

    return execute_query(invoke_cursor_func)


def get_pending_scraping_requests(scraping_date_str, offset, row_count):
    pending_scraping_request_property_names = [
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

    def convert_func(scraping_request):
        return convert_tuple_to_dict(
            scraping_request,
            pending_scraping_request_property_names,
        )

    def invoke_cursor_func(cursor):
        pending_scraping_requests = []
        cursor.callproc(
            "get_pending_scraping_requests",
            [scraping_date_str, offset, row_count],
        )
        for result in cursor.stored_results():
            pending_scraping_requests = list(map(convert_func, result.fetchall()))

        return pending_scraping_requests

    return execute_query(invoke_cursor_func)


class QuoteCache:
    """A simple tool to boost performance for saving quotes to database.
    There are two kinds of quotes. One is for normal quotes. Normal quotes has
    vehicle category id and price. The other is for scraping request fulfillment (SRF).
    SRF quotes don't have vehicle category id and their price is 0.
    """

    def __init__(self):
        QuoteCache.CAPACITY = 1000
        self._cache = []
        # SQL statement used to insert a normal quote
        self._query_for_normal_quote = """insert into rental_quote(company_id, rental_route_id,
            pick_up_date_id, pick_up_time_id, rental_duration_id,
            vehicle_category_id, price, created_on) values
            (%s, %s, %s, %s, %s, get_vehicle_category_id(%s, %s, %s, %s), %s, %s)"""
        # SQL statement used to insert a SRF quote
        self._query_for_srf_quote = """insert into rental_quote(company_id,
            rental_route_id, pick_up_date_id, pick_up_time_id, rental_duration_id, created_on)
            values(%s, %s, %s, %s, %s, %s)"""

    def get_count(self):
        return len(self._cache)

    def add_quotes(self, quotes):
        quotes_count = len(quotes)
        if quotes_count > QuoteCache.CAPACITY:
            raise RuntimeError(
                "Quote cache is not big enough to accommodate {} quotes.".format(
                    quotes_count
                )
            )
        if self.get_count() + quotes_count > QuoteCache.CAPACITY:
            return False

        for quote in quotes:
            keys_count = len(quote.keys())
            if keys_count == 6:
                # Create a SRF quote
                self._cache.append(
                    (
                        quote["company_id"],
                        quote["rental_route_id"],
                        quote["pick_up_date_id"],
                        quote["pick_up_time_id"],
                        quote["rental_duration_id"],
                        quote["created_on"],
                    )
                )
            elif keys_count == 10:
                # Create a normal quote
                self._cache.append(
                    (
                        quote["company_id"],
                        quote["rental_route_id"],
                        quote["pick_up_date_id"],
                        quote["pick_up_time_id"],
                        quote["rental_duration_id"],
                        quote["company_id"],
                        quote["vehicle_category_name"],
                        quote["vehicle_category_description"],
                        quote["vehicle_age_description"],
                        quote["price"],
                        quote["created_on"],
                    )
                )
            else:
                raise RuntimeError(
                    "The following quote is invalid:\n{}".format(pprint(quote))
                )

        return True

    def flush(self):
        """Save the quotes in cache to the database then empty the cache."""

        def filter_normal_quotes(quote):
            return len(quote) == 11

        def filter_srf_quotes(quote):
            return len(quote) == 6

        def invoke_cursor_func(cursor):
            if self.get_count() > 0:
                _cache_for_normal_quote = list(
                    filter(filter_normal_quotes, self._cache)
                )
                if _cache_for_normal_quote:
                    cursor.executemany(
                        self._query_for_normal_quote, _cache_for_normal_quote
                    )

                _cache_for_srf_quote = list(filter(filter_srf_quotes, self._cache))
                if _cache_for_srf_quote:
                    cursor.executemany(self._query_for_srf_quote, _cache_for_srf_quote)

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
