"""
Correct timestamps of already annotated files.

This should be run inside a ROS enviroment. You will likely need to install
rospy_message_converter with `pip install rospy-message-converter`

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


# Note that this is deliberately not imported from universal_devkit.utils.utils.py
# to avoid needing to install the entire package inside a ROS enviroment
def get_timestamp(imu_dict):
    """The timestamp of a message does not necessarily equal
    the timestamp in the message's header. The header timestamp
    is more accurate and the timestamp of the message just corresponds
    to whenever the bag received the message and saved it.

    Args:
        imu_dict (dict): dictionary of a single IMU reading

    Returns:
        str: a string timestamp to use for this IMU message.
        Uses the header timestamp
    """

    # We need to convert the seconds to nanoseconds so we can add them
    # We need to make sure the seconds value is an int, so the output
    # string isn't formatted with scientific notation
    seconds = int(imu_dict["header"]["stamp"]["secs"] * 1e9)
    nanoseconds = imu_dict["header"]["stamp"]["nsecs"]
    total_time = seconds + nanoseconds
    return str(total_time)


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
    print("Correcting messages from " + input_directory + "...")

    # ============ Loop through ROS bag ===========

    for topic, msg, timestamp in tqdm(input_bag.read_messages()):

        json_str = json_message_converter.convert_ros_message_to_json(msg)
        json_dict = json.loads(json_str)
        correct_timestamp = get_timestamp(json_dict)

        pattern = "{}/{}.*".format(input_directory, timestamp)
        existing_files = glob(pattern)

        assert (
            len(existing_files) <= 1
        ), "The number of files matching a timestamp should be <= 1"

        # If there is a file with a matching name
        if len(existing_files) == 1:
            filepath = existing_files[0]

            # See: https://stackoverflow.com/a/35188296/6942666
            # This will capture when you have multiple extensions like ".pcd.json"
            extension = "".join(Path(filepath).suffixes)

            # Copy over the file to the output directory
            output_filename = correct_timestamp + extension
            output_file = os.path.join(output_directory, output_filename)
            shutil.copyfile(filepath, output_file)

    input_bag.close()


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--output", type=str, required=True, help="The output directory"
    )
    ap.add_argument(
        "-i", "--input", type=str, required=True, help="The input directory"
    )
    ap.add_argument(
        "-b", "--bag", type=str, required=True, help="Path to the original bag"
    )
    args = vars(ap.parse_args())
    correct_timestamps(args["input"], args["bag"], args["output"])
