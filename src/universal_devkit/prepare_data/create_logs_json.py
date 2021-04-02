import csv
import glob
import os

from universal_devkit.utils.utils import create_token, write_json


def get_logs(logs_dir_path):
    """Creates descriptions of log files in a directory.

    Args:
        logs_dir_path (str): the path to the directory with the log files and .csv file

    Returns:
        list: a list of dictionaries with information about all the logs
    """

    # Assert that only one CSV file
    csv_files = glob.glob(os.path.join(str(logs_dir_path), "*.csv"))
    num_csv = len(csv_files)
    assert num_csv == 1

    # Read in a CSV of form: "logfile, date_captured, vehicle, location, notes"
    log_data = []
    with open(csv_files[0]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", skipinitialspace=True)
        row_number = 0
        # Go through each row
        for row in csv_reader:
            # If not on row 0 (column names), read in data
            if row_number != 0:

                # Make sure all the logfiles in the CSV file correspond to
                # actual log files in the directory
                num_log_file = len(glob.glob(os.path.join(str(logs_dir_path), row[0])))
                assert num_log_file == 1

                # Use create_token() to create the token
                token = create_token()

                # Save a list of dictionaries
                csv_row_dict = {
                    "token": token,
                    "logfile": row[0],
                    "vehicle": row[2],
                    "date_captured": row[1],
                    "location": row[3],
                }
                log_data.append(csv_row_dict)

            row_number = row_number + 1

    write_json(log_data, os.path.join(str(logs_dir_path), "get_logs.json"))
    return log_data
