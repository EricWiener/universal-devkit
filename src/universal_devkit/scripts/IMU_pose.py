"""
Script to extract IMU Pose from ROS bags.
The data is structured as expected by supervisely.io

Usage:
You can call this script from the command line. You need to download a lidar ROS bag
and a camera data ROS bag (from the same recording session). You can then pass in both
bags as arguments, and the data will be extracted for you so it is ready to be uploaded
for annotating.


Source for ros to json converter
https://github.com/uos/rospy_message_converter

$ python IMU_pose.py -i raise-the-flag_imu.bag -t /imu/data/raw -o output_folder
"""

import argparse
import json
import os

import rosbag
from rospy_message_converter import json_message_converter
from tqdm import tqdm

from universal_devkit.utils.utils import get_timestamp


def main(input_bag_path, topic_specified, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

        # Read point cloud data from bag.
    input_bag = rosbag.Bag(input_bag_path)

    print("Reading data from " + input_bag_path + "...")

    # ============ Loop through ROS bag ===========

    data = {}
    timestamps = []
    for topic, msg, timestamp in tqdm(input_bag.read_messages(topics=topic_specified)):

        try:
            json_str = json_message_converter.convert_ros_message_to_json(msg)
        except Exception:
            print("Failed to convert msg: ", msg)

        json_dict = eval(json_str)
        timestamp = get_timestamp(json_dict)
        data[str(timestamp)] = json_dict
        timestamps.append(str(timestamp))

    data["timestamps"] = timestamps
    # Save
    file_name = "IMU"
    file_path = os.path.join(output_directory, file_name + ".json")
    with open(file_path, "w") as outfile:
        json.dump(data, outfile)

    input_bag.close()


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--output", type=str, default="output", help="The output directory"
    )
    ap.add_argument("-i", "--input_bag", type=str, help="The path to the input bag")
    ap.add_argument("-t", "--topic", type=str, help="Topic for the ROS bag")
    args = vars(ap.parse_args())
    main(args["input_bag"], args["topic"], args["output"])
