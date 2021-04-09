"""
Correct timestamps of already annotated files.

$ python correct_sweeps.py -i input_directory
"""

import argparse
import os
import shutil

from universal_devkit.utils.utils import get_closest_match


def correct_sweeps(input_dir):
    annotation_dir = os.path.join(input_dir, "samples", "LIDAR_TOP", "annotations")
    camera_dir = os.path.join(input_dir, "samples", "CAMERA_FRONT")
    sweeps_pcd_dir = os.path.join(input_dir, "sweeps", "LIDAR_TOP")
    sweeps_image_dir = os.path.join(input_dir, "sweeps", "CAMERA_FRONT")
    camera_images = []
    for filename in os.listdir(camera_dir):
        filename_no_extension, extension = os.path.splitext(filename)
        if extension == ".png":
            camera_images.append(int(filename_no_extension))
    camera_images.sort()
    for filename in os.listdir(annotation_dir):
        if os.path.getsize(os.path.join(annotation_dir, filename)) == 2:
            filename_no_extension, extension = os.path.splitext(filename)
            pcd_file = os.path.join(
                input_dir, "samples", "LIDAR_TOP", filename_no_extension
            )
            shutil.move(pcd_file, sweeps_pcd_dir)
            filename_no_extension_no_pcd, extension = os.path.splitext(
                filename_no_extension
            )
            image = get_closest_match(camera_images, int(filename_no_extension_no_pcd))
            image_file = os.path.join(camera_dir, str(image) + ".png")
            shutil.move(image_file, sweeps_image_dir)


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", type=str, help="The input directory")
    args = vars(ap.parse_args())
    correct_sweeps(args["input"])
