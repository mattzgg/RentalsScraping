from termcolor import colored
from utils.datatype import is_tuple_or_list


def is_empty_string(input_value):
    return (
        input_value is None
        or not isinstance(input_value, str)
        or input_value.strip() == ""
    )


def is_valid_db_entity_id(input_value, valid_db_entity_ids=None):
    if is_empty_string(input_value):
        return False

    if not is_tuple_or_list(valid_db_entity_ids):
        return input_value.isnumeric()

    return int(input_value) in valid_db_entity_ids


def is_quit_command(input_value):
    return input_value == "q"


def create_option(option_text):
    return colored(option_text.rjust(len(option_text) + 4), "green")


def create_warning(text):
    return colored(text, "yellow")
