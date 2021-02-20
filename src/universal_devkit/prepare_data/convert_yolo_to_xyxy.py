"""Converts a directory of YOLO formatted data to XYXY format.
"""
import os
import numpy as np
from bbox_utils import BoundingBox
import glob
from pathlib import Path
import argparse
import shutil
import cv2
import json
from tqdm import tqdm


def convert_images_from_yolo_to_xyxy(
    yolo_directory_path, output_path, extension=".jpg"
):
    """Converts a directory of YOLO formatted labels to XYXY labels.

    Args:
        yolo_directory_path (str): the path to the YOLO formatted data
        output_path (str): the path to store the ouput
    """
    LABEL_DIR = os.path.join(yolo_directory_path, "labels")
    IMAGE_DIR = os.path.join(yolo_directory_path, "images")
    OUTPUT_LABEL_DIR = os.path.join(output_path, "labels")
    OUTPUT_IMAGE_DIR = os.path.join(output_path, "images")

    # Ensure the image and label directories exist
    assert Path(
        yolo_directory_path
    ).is_dir(), "The YOLO directory path specified does not exist"
    assert Path(LABEL_DIR).is_dir(), "The YOLO directory must contain a 'labels' folder"
    assert Path(
        IMAGE_DIR
    ).is_dir(), "The YOLO directory must contain an 'images' folder"

    # Remove the output path if it exists
    shutil.rmtree(output_path, ignore_errors=True)

    # Create the output directories
    Path(OUTPUT_LABEL_DIR).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    # Get all the label paths
    label_paths = glob.glob(LABEL_DIR + "/*.txt")

    for label_path in tqdm(label_paths):
        file_name = Path(label_path).stem

        # Get a list of annotations (list of strings)
        with open(label_path) as f:
            annotations = list(f)

        # Get the corresponding image dimensions
        image_path = os.path.join(IMAGE_DIR, file_name + extension)
        img = cv2.imread(image_path)
        img_height, img_width = img.shape[:2]
        image_dimension = np.array([img_height, img_width])

        # A list of XYXY annotation strings
        annotation_dict = {
            "image_name": file_name + ".png",
            "dimensions": img.shape,
            "annotations": [],
        }

        for annotation in annotations:
            class_id, center_x, center_y, width, height = annotation.split()

            # Convert strings into their correct numeric type
            class_id = int(class_id)
            center_x = float(center_x)
            center_y = float(center_y)
            width = float(width)
            height = float(height)
            center = np.array([center_x, center_y])

            # Convert from YOLO to XYXY
            bbox = BoundingBox.from_yolo(center, width, height, image_dimension)
            xy1, xy2 = bbox.to_xyxy()

            # Flatten into a single list of form [X1, Y1, X2, Y2]
            x1 = xy1[0].item()
            y1 = xy1[1].item()
            x2 = xy2[0].item()
            y2 = xy2[1].item()
            # @TODO: update the class_id to be the correct string identifier
            annotation_dict["annotations"].append(
                {"class": class_id, "xyxy": [x1, y1, x2, y2]}
            )

        # Write the output annotations
        output_annotation_file = os.path.join(OUTPUT_LABEL_DIR, file_name + ".png.json")
        with open(output_annotation_file, "w") as f:
            json.dump(annotation_dict, f)

        # Copy over the image
        output_image_path = os.path.join(OUTPUT_IMAGE_DIR, file_name + ".png")
        cv2.imwrite(output_image_path, img)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The path to the YOLO data directory",
    )
    ap.add_argument(
        "-o", "--output", type=str, default="output", help="The output directory"
    )
    ap.add_argument(
        "-e", "--extension", type=str, default=".jpg", help="The image extension to use"
    )
    args = vars(ap.parse_args())
    convert_images_from_yolo_to_xyxy(args["input"], args["output"], args["extension"])