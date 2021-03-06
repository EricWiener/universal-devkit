from create_logs_json import get_logs

def create_logs_json_test(logs_dir_path):
    correct_output = []

    # Row 1
    temp_row = {"token": 0,
                "logfile": "log1.txt",
                "vehicle": "big boat",
                "date_captured": "2021-07-01",
                "location": "music pond"
                }
    correct_output.append(temp_row)

    # Row 2
    temp_row = {"token": 0,
                "logfile": "log2.txt",
                "vehicle": "small boat",
                "date_captured": "2021-02-01",
                "location": "other pond"
                }
    correct_output.append(temp_row)

    # Row 3
    temp_row = {"token": 0,
                "logfile": "random-name.txt",
                "vehicle": "medium boat",
                "date_captured": "2020-07-01",
                "location": "not a pond"
                }
    correct_output.append(temp_row)

    # Row 4
    temp_row = {"token": 0,
                "logfile": "ima_log.txt",
                "vehicle": "boat boat",
                "date_captured": "2019-07-01",
                "location": "ocean"
                }
    correct_output.append(temp_row)

    output = get_logs(logs_dir_path)

    # Assert get_logs gave correct output (excluding "token")
    for row in range(4):
        for key in correct_output[row]:
            if key != "token":
                assert correct_output[row][key] == output[row][key]

