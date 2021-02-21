import glob
import random
import os
import csv
import json

def get_logs(logs_dir_path):
    """Creates descriptions of log files in a directory.

    Args:
        logs_dir_path (str): the path to the directory with the log files and .csv file

    Returns:
        list: a list of dictionaries with information about all the logs
    """

    # @TODO: assert that only one CSV file
    os.chdir(logs_dir_path)
    numCSV = len(glob.glob("*.csv"))
    assert numCSV == 1

    # @TODO: read in a CSV of form: "logfile, date_captured, vehicle, location, notes"
    log_data = []
    for file in glob.glob("*.csv"):
        with open(logs_dir_path + file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_number = 0
            for row in csv_reader:
                if line_number != 0:
                    numLogFile = len(glob.glob(row[0]))
                    assert numLogFile == 1

                    token = create_token()

                    csv_row_dict = {"token": token, "logfile": row[0], "vehicle": row[2], "date_captured": row[1],
                                    "location": row[3]}

                    log_data.append(csv_row_dict)
                line_number = line_number + 1

    # @TODO: make sure all the logfiles in the CSV file correspond to actual log files
    # in the directory

    # @TODO: save a list of dictionaries of form:
    # @TODO: use create_token() to create the token
    # {
    # "token": "53cf9c55dd8644bea67b9f009fc1ee38", # this needs to be generated
    # "logfile": "n008-2018-08-01-15-16-36-0400",
    # "vehicle": "n008", # an identifier for the boat used
    # "date_captured": "2018-08-01",
    # "location": "music-pond"
    # },

    with open(logs_dir_path + "\\" + "logs.json", 'w') as outfile:
        json.dump(log_data, outfile)
    return log_data

