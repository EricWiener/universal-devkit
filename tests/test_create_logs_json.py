from universal_devkit.prepare_data.create_logs_json import get_logs
import shutil
from pathlib import Path
from universal_devkit.utils import read_json

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

def test_create_logs_json():
# The path to the folder with example logs
    example_logs_path = get_relative_path(
        "assets/example_logs"
    )

    # The correct output for the example logs
    correct_output_path = get_relative_path(
        "assets/create_logs_json_correct.json"
    )

    # The path to use as the output directory
    output_file_dir = "universal_devkit/tests"
    
    # The file to be used as output
    output_file_path = "universal_devkit/tests/example_logs_output.json" # What is file name going to be?
    
    # Convert the example logs
    output = get_logs(example_logs_path)

    # Make sure the output is correct
    correct_data = read_json(correct_output_path)
    output_data = read_json(output_file_path)

    ignore_keys = ["token"]

    assert len(correct_data) == len(output_data)

    for i in range(len(output_data)):
        output_d = output_data[i]
        correct_d = correct_data[i]
        assert equal_dicts(output_d, correct_d, ignore_keys=ignore_keys)

    shutil.rmtree(output_file_path)


