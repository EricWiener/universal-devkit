"""
Script to extract IMU Pose from ROS bags.
The data is structured as expected by supervisely.io

Usage:
You can call this script from the command line. You need to download a lidar ROS bag
and a camera data ROS bag (from the same recording session). You can then pass in both
bags as arguments, and the data will be extracted for you so it is ready to be uploaded
for annotating.

You should have sourced your ROS enviroment before running this script.

Source for ros to json converter
https://github.com/uos/rospy_message_converter

$ python ros_imu_pose.py -i raise-the-flag_imu.bag -t /imu/data/raw -o output_folder
"""

import argparse
import json
import os
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
    return total_time


def ros_imu_pose(input_bag_path, topic_specified, output_directory):
    Path.mkdir(Path(output_directory), parents=True, exist_ok=True)

    # Read point cloud data from bag.
    input_bag = rosbag.Bag(input_bag_path)

    print("Reading data from " + input_bag_path + "...")

    # ============ Loop through ROS bag ===========

    """
    This will be a list of the form:

        [
                {
                    "timestamp": 1532402927814384,
                    "rotation": [
                        0.5731787718287827,
                        -0.0015811634307974854,
                        0.013859363182046986,
                        -0.8193116095230444
                    ],
                    "translation": [
                        410.77878632230204,
                        1179.4673290964536,
                        0.0
                    ]
                },
                ...
        ]
    """
    data = []

    for topic, msg, timestamp in tqdm(input_bag.read_messages(topics=topic_specified)):
        try:
            json_str = json_message_converter.convert_ros_message_to_json(msg)
        except Exception:
            print("Failed to convert message: ", msg)

        # Load from the JSON string
        json_dict = json.loads(json_str)
        header_timestamp = get_timestamp(json_dict)
        data.append(
            {
                "timestamp": header_timestamp,
                "rotation": json_dict["orientation"],
                # set these to 0 because the IMU doesn't have position
                "translation": [0.0, 0.0, 0.0],
            }
        )

    input_bag.close()

    # Save to imu.json
    file_name = "imu"
    file_path = os.path.join(output_directory, file_name + ".json")

    with open(file_path, "w") as outfile:
        print("Saving output JSON to: ", file_path)
        json.dump(data, outfile)


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--output", type=str, default="output", help="The output directory"
    )
    ap.add_argument(
        "-i", "--input_bag", type=str, required=True, help="The path to the input bag"
    )
    ap.add_argument(
        "-t", "--topic", type=str, default="/imu/data/raw", help="Topic for the ROS bag"
    )
    args = vars(ap.parse_args())
    ros_imu_pose(args["input_bag"], args["topic"], args["output"])
