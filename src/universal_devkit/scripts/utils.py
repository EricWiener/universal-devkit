import json
import uuid


def read_json(path):
    """Loads a dictionary from a JSON file

    Args:
        path (str): path to a JSON file

    Returns:
        dict: dictionary loaded from JSON
    """
    with open(path) as f:
        data = json.load(f)
    return data


def write_json(data, path):
    """Writes data to a JSON file

    Args:
        data (any): data to write
        path (str): path to save the JSON file to
    """
    with open(path, "w") as f:
        json.dump(data, f)


def create_token():
    """Generates a 32 character unique identifier

    Returns:
        str: unique identifier
    """
    return uuid.uuid4().hex


def get_existing_token(data_list, json_path, match_key, token_key):
    """Takes a list of dictionaries and tries to assign the [token_key]
    value passed on matching existing data in the JSON file using the [match_key].

    For example, you can use this to find the sensor
    tokens to use for the calibrated sensor data.

    Args:
        data_list (list(dict)): list of dictionaries to add the keys to.
                        Will modify this list
        json_path (str): path to the JSON file
        match_key (str): the key to use to match up values
        token_key (str): the key the matched token should be stored to

    Returns:
        list(dict): updated list of dictionaries
    """

    # Read in data
    json_data = read_json(json_path)

    # Create a dictionary mapping from match_key value -> json dict
    match_key_to_json = {d[match_key]: d for d in json_data}

    # Now try to find matches
    for d in data_list:
        assert d[match_key] in match_key_to_json, "Unable to find key for {}".format(d)
        d[token_key] = match_key_to_json[d[match_key]]

    return data_list


def merge_json_lists(path_a, path_b):
    """Merge two JSON files with lists

    Args:
        path_a (str): path to JSON file A
        path_b (str): path to JSON file B

    Returns:
        list: list of data with B's data added to the end of A
    """

    data_a = read_json(path_a)
    data_b = read_json(path_b)

    return data_a.extend(data_b)


def remove_key_from_dicts(data_list, key):
    """Remove a certain key from a list of dictionaries

    Args:
        data_list (list(dict)): list of dictionaries. This will get modified
        key (str): string to remove
    """
    for d in data_list:
        del d[key]
