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

import os
import rosbag
import json
import argparse
import numpy as np
import open3d as o3d
import cv2
from bisect import bisect_left
from tqdm import tqdm
from shutil import copyfile

from rospy_message_converter import json_message_converter
from std_msgs.msg import String

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
		except:
			print(msg)

		json_dict = json.loads(json_str)
		timestamp = get_timestamp(json_dict)
		data[str(timestamp)] = json_dict
		timestamps.append(str(timestamp))

		  
	input_bag.close()
	data["timestamps"] = timestamps
		# Save
	file_name = "IMU"
	file_path = os.path.join(output_directory, file_name + ".json")
	with open(file_path, 'w') as outfile:
		json.dump(data, outfile)



if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-o",
                    "--output",
                    type=str,
                    default="output",
                    help="The output directory")
	ap.add_argument("-i",
                    "--input_bag",
                    type=str,
                    help="The path to the input bag")
	ap.add_argument("-t",
                    "--topic",
                    type=str,
                    help="Topic for the ROS bag")
	args = vars(ap.parse_args())
	main(args["input_bag"], args["topic"], args["output"])
