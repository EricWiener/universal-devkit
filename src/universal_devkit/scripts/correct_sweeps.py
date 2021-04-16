"""
Move all keyframes with empty annotations into the sweeps directory.
Will also move corresponding images and delete empty annotation files.

$ python correct_sweeps.py -i input_directory
"""

import argparse
import os
import shutil
from glob import glob
from pathlib import Path

from universal_devkit.utils.utils import get_closest_match


def correct_sweeps(input_dir):
    annotation_dir = os.path.join(input_dir, "samples", "LIDAR_TOP", "annotations")
    camera_dir = os.path.join(input_dir, "samples", "CAMERA_FRONT")
    sweeps_pcd_dir = os.path.join(input_dir, "sweeps", "LIDAR_TOP")
    sweeps_image_dir = os.path.join(input_dir, "sweeps", "CAMERA_FRONT")

    camera_images = [
        int(Path(filepath).stem) for filepath in glob("{}/*.png".format(camera_dir))
    ]

    pcd_sweeps = []
    pcd_samples = []

    for filename in os.listdir(annotation_dir):
        filename_no_extension, extension = os.path.splitext(filename)
        filename_no_extension_no_pcd, extension = os.path.splitext(
            filename_no_extension
        )
        if os.path.getsize(os.path.join(annotation_dir, filename)) == 2:
            pcd_file = os.path.join(
                input_dir, "samples", "LIDAR_TOP", filename_no_extension
            )
            shutil.move(pcd_file, sweeps_pcd_dir)
            pcd_sweeps.append(int(filename_no_extension_no_pcd))
            # Remove the empty annotation file
            os.remove(os.path.join(annotation_dir, filename))
        else:
            pcd_samples.append(int(filename_no_extension_no_pcd))

    pcd_sweeps.sort()
    pcd_samples.sort()

    for image in camera_images:
        closest_sweep = get_closest_match(pcd_sweeps, image)
        closest_sample = get_closest_match(pcd_samples, image)
        if abs(closest_sweep - image) < abs(closest_sample - image):
            image_file = os.path.join(camera_dir, str(image) + ".png")
            shutil.move(image_file, sweeps_image_dir)


if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--input", type=str, required=True, help="The input directory"
    )
    args = vars(ap.parse_args())
    correct_sweeps(args["input"])
