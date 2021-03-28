"""
Correct timestamps of already annotated files.

$ python correct_timestamps.py -i input_directory -b bag -o output_directory
"""

import argparse
import json
import os
import shutil
from glob import glob
from pathlib import Path

import rosbag
from rospy_message_converter import json_message_converter
from tqdm import tqdm

from universal_devkit.utils.utils import get_timestamp


def correct_timestamps(input_directory, bag_path, output_directory):
    """Script to correct timestamps if files were generated using ROS
        bag time vs. ROS header time


    Args:
        input_directory (str): path to the directory of files to fix
        bag_path (str): path to the bag the files were generated from
        output_directory (str): path to the directory to store files
            with correct names
    """
    Path.mkdir(Path(output_directory), parents=True, exist_ok=True)

    # Read point cloud data from bag.
    input_bag = rosbag.Bag(bag_path)

    print("Reading data from " + bag_path + "...")

    # ============ Loop through ROS bag ===========

    for topic, msg, timestamp in tqdm(input_bag.read_messages()):

        json_str = json_message_converter.convert_ros_message_to_json(msg)
        json_dict = json.loads(json_str)
        correct_timestamp = get_timestamp(json_dict)

        existing_files = glob.glob("{}*".format(timestamp))

        assert (
            existing_files <= 1
        ), "The number of files matching a timestamp should be <= 1"

        # If there is a file with a matching name
        if len(existing_files) == 1:
            filename = existing_files[0]
            filename_no_extension, extension = os.path.splitext(filename)
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, correct_timestamp + extension)
            shutil.copyfile(input_file, output_file)

    input_bag.close()


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, help="The output directory")
    ap.add_argument("-i", "--input", type=str, help="The input directory")
    ap.add_argument("-b", "--bag", type=str, help="Path to the original bag")
    args = vars(ap.parse_args())
    correct_timestamps(args["input"], args["bag"], args["output"])
