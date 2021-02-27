import argparse
import json

# python test_supervisely_3d_to_universal.py
# -n assets/example_logs/format_supervisely_annotations_output_correct.json
# -c assets/example_logs/format_supervisely_annotations_output_correct.json


def main(new_file, correct_file):
    with open(new_file) as nf:
        new_data = json.load(nf)
    with open(correct_file) as cf:
        correct_data = json.load(cf)

    if new_data == correct_data:
        print("Files match!")
    else:
        print("Error! Files are different.")


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--correct", type=str, help="The correct test file")
    ap.add_argument("-n", "--new", type=str, help="The new test file")
    args = vars(ap.parse_args())
    main(args["new"], args["correct"])
