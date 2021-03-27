import json
import os
import uuid
from bisect import bisect_left
from pathlib import Path


def get_timestamp(imu_dict):
    """The timestamp of a message does not necessarily equal
    the timestamp in the message's header. The header timestamp
    is more accurate and the timestamp of the message just corresponds
    to whenever the bag received the message and saved it.

    Args:
        imu_dict (dict): dictionary of a single IMU reading

    Returns:
        str: a string timestamp to use for this IMU message.
        Uses the header timestamp
    """

    # We need to convert the seconds to nanoseconds so we can add them
    # We need to make sure the seconds value is an int, so the output
    # string isn't formatted with scientific notation
    seconds = int(imu_dict["header"]["stamp"]["secs"] * 1e9)
    nanoseconds = imu_dict["header"]["stamp"]["nsecs"]
    total_time = seconds + nanoseconds
    return str(total_time)


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

    For example, you can use this to find the sensor tokens
    to use for the calibrated sensor data.

    Args:
        data_list (list(dict)): list of dictionaries to add
            the keys to. Will modify this list
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


def get_all_non_hidden_files(data_directory, exclude=[]):
    visible_files = []
    for file in Path(data_directory).iterdir():
        if not file.name.startswith(".") and file.name not in exclude:
            visible_files.append(file)

    return visible_files


def get_immediate_directories(directory_path):
    """Gets the immediate sub-directories within a directory

    Args:
        directory_path (str): path to the directory

    Returns:
        list(str): list of sub-directories
    """
    p = Path(directory_path)
    return [f for f in p.iterdir() if f.is_dir() and not f.name.startswith(".")]


def convert_list_to_dict(data_list: list, using_key: str):
    """Converts a list of dictionaries to a dictionary using the value
    of a specific key in each object as the indentifier

    Args:
        data_list (list): the list of dictionaries
        using_key (str): the key to use to identify each dictionary

    Returns:
        dict: a dictionary form of the list
    """

    output = {}

    for item in data_list:
        output[item[using_key]] = item

    return output


def get_file_stem_name(file_path: str):
    """Gets the stem of a file path.

    Example::

        >>> get_file_stem_name("/home/user/Downloads/repo/test.txt")
        "test"

    Args:
        file_path (str): the path to extract the stem from

    Returns:
        str: the stem of the file
    """
    return Path(file_path).stem


def get_full_path_to_file(root_data_dir: str, relative_file_path: str):
    """Gets the path to a file given the path to the root data directory
    and a path relative to the root of the data directory

    Args:
        root_data_dir (str): the path to the root directory of the dataset
        relative_file_path (str): a path relative to the root directory of the dataset

    Returns:
        str: the full path to the file
    """
    return os.path.join(root_data_dir, relative_file_path)


def get_file_extension(file_path: str):
    """Gets the extension of a file.

    Example::

        >>> get_file_stem_name("/home/user/Downloads/repo/test.txt")
        "txt"

    Args:
        file_path (str): the path to extract the extension from

    Returns:
        str: the extension of the file
    """
    return Path(file_path).suffix


def get_closest_match(sorted_list, query_number):
    """
    Source: https://stackoverflow.com/a/12141511

    Parameters:
    - sorted_list: a sorted list of numbers to search through
    - query_number: the number to search for

    Returns:
    The closest value in sorted_list to query_number.
    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(sorted_list, query_number)
    if pos == 0:
        return sorted_list[0]
    if pos == len(sorted_list):
        return sorted_list[-1]
    before = sorted_list[pos - 1]
    after = sorted_list[pos]
    if after - query_number < query_number - before:
        return after
    else:
        return before
