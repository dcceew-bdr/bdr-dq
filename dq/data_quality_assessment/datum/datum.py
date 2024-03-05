def is_not_empty(datum):
    """
    Checks if the provided datum is not empty. This function can handle different data types,
    including strings, lists, dictionaries, and None values.

    :param datum: The data to check.
    :return: True if the datum is considered not empty, False otherwise.
    """
    if datum is None:
        return False
    if isinstance(datum, (str, list, dict, set)):
        return bool(datum)  # Checks if strings/lists/dicts/sets are not empty
    return True  # For other data types, assume 'not empty' if not None


def is_valid_datum(datum):
    """
    Checks if the provided datum is one of the specified valid geo datums.

    :param datum: The datum string to check.
    :return: True if the datum is valid, False otherwise.
    """
    valid_datums = {"AGD84", "GDA2020", "GDA94", "WGS84"}
    return datum in valid_datums
