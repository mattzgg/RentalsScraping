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
