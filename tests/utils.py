from pathlib import Path


def get_relative_path(relative_file_path):
    return Path(__file__).parent / relative_file_path


def equal_dicts(d1: dict, d2: dict, ignore_keys: list):
    """Check two dictionaries for equality with the ability to ignore
    specific keys.

    Source: https://stackoverflow.com/a/10480904/6942666

    Args:
        d1 (dict): the first dictionary
        d2 (dict): the second dictionary
        ignore_keys (list): a list of strings with keys to ignore

    Returns:
        bool: whether the dicts are equal
    """
    d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
    return d1_filtered == d2_filtered
