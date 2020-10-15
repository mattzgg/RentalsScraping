from utils.ui import is_empty_string, parse_booking_request_template_configs_str
from budget.location import scrape_locations

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

scrape_locations()