"""
Script to format annotations from supervisely.io into
the custom universal format


$ python supervisely_3d_to_universal.py -i input_directory -o output_directory
"""

import argparse
import json
import os
from pathlib import Path

from universal_devkit.utils import create_token


def convert_supervisely_3d_to_universal(input_directory, output_directory):
    Path.mkdir(output_directory, parents=True, exist_ok=True)

    for filename in os.listdir(input_directory):
        with open(os.path.join(input_directory, filename)) as f:
            input_data = json.load(f)

        output_data = []
        for figure in input_data["figures"]:
            ann = {}

            ann["token"] = create_token()
            ann["sample_token"] = ""
            ann["instance_token"] = create_token()
            ann["visibility_token"] = ""
            ann["attribute_tokens"] = []

            figure_geometry = figure["geometry"]
            ann["translation"] = [
                figure_geometry["position"]["x"],
                figure_geometry["position"]["y"],
                figure_geometry["position"]["z"],
            ]

            ann["size"] = [
                figure_geometry["dimensions"]["x"],
                figure_geometry["dimensions"]["y"],
                figure_geometry["dimensions"]["z"],
            ]

            ann["rotation"] = [
                figure_geometry["rotation"]["x"],
                figure_geometry["rotation"]["y"],
                figure_geometry["rotation"]["z"],
            ]

            ann["prev"] = ""
            ann["next"] = ""
            ann["num_lidar"] = 0
            ann["num_radar"] = 0
            ann["labeller"] = figure["labelerLogin"]
            ann["annotation_created"] = figure["createdAt"]
            output_data.append(ann)

        with open(os.path.join(output_directory, filename), "w") as f:
            json.dump(output_data, f)


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--output", type=str, default="output", help="The output directory"
    )
    ap.add_argument("-i", "--input", type=str, help="The input directory")
    args = vars(ap.parse_args())
    convert_supervisely_3d_to_universal(args["input"], args["output"])
