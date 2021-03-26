import argparse
import csv
import json


def main(csv_in, json_out):
    """Reads in a CSV file, converts it to a dictionary, and adds tokens

    Args:
        csv_in (str): the path to the CSV input file
        json_out (str): the path to save the resulting JSON file
    """
    data_list = list(csv.DictReader(open(csv_in), skipinitialspace = True))

    for obj in data_list:
        if "token" not in obj:
            # Avoid overwriting existing tokens
            obj["token"] = 100 # FIXXXX!!!!

    with open(json_out, "w") as f:
        json.dump(data_list, f)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--csv", type=str, help="The path to the input CSV")
    ap.add_argument("-j", "--json", type=str, help="The path to the output JSON")
    args = vars(ap.parse_args())
    main(args["csv"], args["json"])
