import csv
import os
from glob import glob
from pathlib import Path

from universal_devkit.utils.utils import create_token, write_json


def get_logs(logs_dir_path):
    """Creates descriptions of log files in a directory.

    Args:
        logs_dir_path (str): the path to the directory with the log files and .csv file

    Returns:
        list: a list of dictionaries with information about all the logs
    """

    # Check that only one CSV file exists
    csv_files = glob(os.path.join(logs_dir_path, "*.csv"))
    assert len(csv_files) == 1, "There should only be a single CSV file"

    # Read in a CSV of form: "logfile, date_captured, vehicle, location, notes"
    log_data = []
    with open(csv_files[0]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", skipinitialspace=True)

        for row_number, row in enumerate(csv_reader):
            if row_number == 0:
                # Skip the header
                continue

            # Make sure all the logfiles in the CSV file correspond to
            # actual log files in the directory
            num_log_file = len(glob(os.path.join(logs_dir_path, row[0])))
            assert (
                num_log_file == 1
            ), "There should only be a single log file matched per CSV row"

            csv_row_dict = {
                "token": create_token(),
                "logfile": row[0],
                "vehicle": row[2],
                "date_captured": row[1],
                "location": row[3],
            }
            log_data.append(csv_row_dict)

    Path(logs_dir_path).mkdir(parents=True, exist_ok=True)
    write_json(log_data, os.path.join(logs_dir_path, "get_logs.json"))
    return log_data
