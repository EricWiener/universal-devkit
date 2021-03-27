"""
Correct timestamps of already annotated files.

$ python correct_timestamps.py -i input_directory -b bag -o output_directory
"""

import argparse
import json
import os
import shutil
from pathlib import Path

import rosbag
from rospy_message_converter import json_message_converter
from tqdm import tqdm

from universal_devkit.utils.utils import get_timestamp


def correct_timestamps(input_directory, bag_path, output_directory):
    Path.mkdir(Path(output_directory), parents=True, exist_ok=True)

    # Read point cloud data from bag.
    input_bag = rosbag.Bag(bag_path)

    print("Reading data from " + bag_path + "...")

    # ============ Loop through ROS bag ===========

    for topic, msg, timestamp in tqdm(input_bag.read_messages()):

        json_str = json_message_converter.convert_ros_message_to_json(msg)
        json_dict = json.loads(json_str)
        correct_timestamp = get_timestamp(json_dict)

        for filename in os.listdir(input_directory):
            filename_no_extension, extension = os.path.splitext(filename)
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, correct_timestamp + extension)
            if str(filename_no_extension) == str(timestamp):
                shutil.copyfile(input_file, output_file)


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, help="The output directory")
    ap.add_argument("-i", "--input", type=str, help="The input directory")
    ap.add_argument("-b", "--bag", type=str, help="The original bag")
    args = vars(ap.parse_args())
    correct_timestamps(args["input"], args["bag"], args["output"])
