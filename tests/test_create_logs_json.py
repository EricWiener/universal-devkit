import os

from utils import equal_dicts, get_relative_path

from universal_devkit.prepare_data.create_logs_json import get_logs
from universal_devkit.utils.utils import read_json


def test_create_logs_json():
    # The path to the folder with example logs
    example_logs_path = get_relative_path("assets/example_logs")

    # The correct output for the example logs
    correct_output_path = get_relative_path("assets/create_logs_json_correct.json")

    # The file to be used as output
    output_file_path = get_relative_path("assets/example_logs/get_logs.json")

    # Convert the example logs
    get_logs(example_logs_path)

    # Make sure the output is correct
    correct_data = read_json(correct_output_path)
    output_data = read_json(output_file_path)

    ignore_keys = ["token"]

    assert len(correct_data) == len(output_data)

    for i in range(len(output_data)):
        output_d = output_data[i]
        correct_d = correct_data[i]
        assert equal_dicts(output_d, correct_d, ignore_keys=ignore_keys)

    os.remove(output_file_path)
