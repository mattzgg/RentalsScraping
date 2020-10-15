from utils.ui import is_empty_string, parse_booking_request_template_configs_str
from budget.location import scrape_locations
from budget.quote import scrape_quotes

# def foo():
#     def bar():
#         return x + 1

#     try:
#         x = 1
#     except:
#         pass
#     else:
#         pass

#     return bar()


# value = foo()
# print(value)


# foo = {"id": 1, "first_name": "Matthew"}
# print(foo["id"])
# print(foo["first_name"])
# print(is_empty_string("     "))

# isinstance("abc", str)

# configs_str = "(1, 2) (3, 4) (5, 6)"
# configs = parse_booking_request_template_configs_str(configs_str)
# print(configs)

# scrape_locations()

scrape_quotes(
    [
        {
            "pick_up_location_input_value": "Auckland Airport, Auckland Ni, New Zealand-(AKL)",
            "pick_up_datetime": "16/10/2020 12:00",
            "drop_off_location_input_value": "63 Arrenway Dr, Unit 6, Auckland Ni, New Zealand-(AK6)",
            "drop_off_datetime": "16/10/2020 12:00",
        }
    ]
)
