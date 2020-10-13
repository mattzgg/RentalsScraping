def convert_tuple_to_dict(tuple_value, dict_keys):
    key_count = len(dict_keys)

    if tuple_value is None:
        index = 0
        tuple_value = tuple()
        while index < key_count:
            tuple_value = tuple_value + (None,)
            index += 1

    result = dict()
    index = 0
    for item in tuple_value:
        key = dict_keys[str(index)]
        result[key] = item
        index += 1

    return result


def is_tuple_or_list(value):
    return type(value) is tuple or type(value) is list