from datetime import datetime


def is_tuple(value):
    return type(value) is tuple


def is_list(value):
    return type(value) is list


def is_tuple_or_list(value):
    return is_tuple(value) or is_list(value)


def convert_tuple_to_dict(tuple_value, tuple_item_names):
    count = len(tuple_item_names)

    if tuple_value is None:
        index = 0
        tuple_value = tuple()
        while index < count:
            tuple_value = tuple_value + (None,)
            index += 1

    result = dict()
    index = 0
    for item in tuple_value:
        key = tuple_item_names[index]
        result[key] = item
        index += 1

    return result


def is_empty_string(input_value):
    return (
        input_value is None
        or not isinstance(input_value, str)
        or input_value.strip() == ""
    )


def assemble_quotes(scraping_request, scraping_response):
    """A quote is composed of a head and a body. The data of the head comes from a scraping
    request. The data of the body comes from a scrapng response."""

    def is_meaningful_price(quote_body):
        price = quote_body["price"]
        return price is not None

    quotes = []

    quote_head = {
        "company_id": scraping_request["company_id"],
        "rental_route_id": scraping_request["rental_route_id"],
        "pick_up_date_id": scraping_request["pick_up_date_id"],
        "pick_up_time_id": scraping_request["pick_up_time_id"],
        "rental_duration_id": scraping_request["rental_duration_id"],
        "created_on": datetime.now(),
    }

    scraping_response = list(filter(is_meaningful_price, scraping_response))

    if len(scraping_response) == 0:
        quotes.append({**quote_head})
    else:
        for quote_body in scraping_response:
            quote = {**quote_head, **quote_body}
            quotes.append(quote)

    return quotes


def format_scraping_request(scraping_request):
    return (
        "[company_id: {}, rental_route_id: {}, pick_up_date_id: {}, "
        + "pick_up_time_id: {}, rental_duration_id: {}]"
    ).format(
        scraping_request["company_id"],
        scraping_request["rental_route_id"],
        scraping_request["pick_up_date_id"],
        scraping_request["pick_up_time_id"],
        scraping_request["rental_duration_id"],
    )