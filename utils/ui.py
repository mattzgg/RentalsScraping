import re

from termcolor import colored
from utils.datatype import is_empty_string, is_tuple_or_list


def is_valid_db_entity_id(input_value, valid_db_entity_ids=None):
    if is_empty_string(input_value):
        return False

    input_value = input_value.strip()

    if not is_tuple_or_list(valid_db_entity_ids):
        return input_value.isnumeric()

    return int(input_value) in valid_db_entity_ids


def parse_db_entity_ids_str(input_value, separator=","):
    raw_ids = input_value.split(separator)
    ids = []
    for raw_id in raw_ids:
        if is_valid_db_entity_id(raw_id):
            ids.append(int(raw_id.strip()))

    return ids


def join_db_entity_ids(db_entity_ids, separator=","):
    str_ids = []
    for db_entity_id in db_entity_ids:
        str_ids.append(str(db_entity_id))

    return separator.join(str_ids)


def is_quit_command(input_value):
    return input_value == "q"


def create_option(option_text):
    return colored(option_text.rjust(len(option_text) + 4), "green")


def create_warning(text):
    return colored(text, "yellow")
