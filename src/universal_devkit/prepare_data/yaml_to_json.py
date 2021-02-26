"""Convert a IMU YAML file to JSON messages. This should be run within the UMA docker.

Example:
```
$ python3 yaml_to_json.py -i \
    "/home/uma/UMA/Bags/raise-the-flag/raise-the-flag_imu.bag" \
    -t "/imu/data/raw" -o output
```
"""
import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import yaml


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


def main(bag_path, topic, output_path):
    # Keep track of how long the conversion took
    # Metrics are fun
    start_time = time.time()

    print("Converting ROS bag to YAML file...")
    with open("imu.yaml", "w") as f:
        # Note that subprocess.run(["rostopic", "echo", "-b", bag_path,
        # topic, ">", "output.yaml"])
        # does not work. You need an actual shell in order to pipe a file.
        # subprocess.run()
        # by default does not use an actual shell because this is not secure.
        # See: https://stackoverflow.com/a/4856684/6942666
        # rostopic echo -b raise-the-flag_imu.bag /imu/data/raw > imu.yaml
        subprocess.run(["rostopic", "echo", "-b", bag_path, topic], stdout=f)

    print("Converting YAML files to JSON...")

    # Remove the output path if it exists
    shutil.rmtree(output_path, ignore_errors=True)

    # Create the output directories
    Path(output_path).mkdir(parents=True, exist_ok=True)

    with open("imu.yaml") as f:
        imu_dicts = yaml.safe_load_all(f)

        for imu_dict in imu_dicts:
            try:
                timestamp = get_timestamp(imu_dict)
            except Exception:
                # Sometimes the last entry might be None
                # Timed the difference between having an if-statement
                # to check the imu_dict vs. using try-except to catch
                # an error. Time difference was negligible.
                # The majority of time is spent on I/O
                continue

            file_name = "{}.json".format(timestamp)
            file_path = os.path.join(output_path, file_name)

            with open(file_path, "w") as f:
                json.dump(imu_dict, f)

    # Clean up after ourselves
    os.remove("imu.yaml")

    total_time = time.time() - start_time
    print("Finished converting bag in {0:0.1f} seconds".format(total_time))


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
