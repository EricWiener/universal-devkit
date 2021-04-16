import filecmp
import shutil

from utils import get_relative_path

from universal_devkit.scripts.convert_yolo_to_xyxy import (
    convert_images_from_yolo_to_xyxy,
)


def test_create_logs_json():
    # The path to the folder with yolo input files
    input_files_path = get_relative_path("assets/yolo_input_file")

    # The directory to be used as output
    output_files_path = get_relative_path("assets/yolo_output_files")

    # Correct yolo files
    correct_output_path = get_relative_path("assets/yolo_correct_files")

    # Convert the yolo input files to xyxy
    convert_images_from_yolo_to_xyxy(input_files_path, output_files_path)

    comp = filecmp.dircmp(output_files_path, correct_output_path)

    assert len(comp.same_files) == 6

    shutil.rmtree(output_files_path)
