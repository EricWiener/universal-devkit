import shutil

from utils import equal_dicts, get_relative_path

from universal_devkit.scripts.supervisely_3d_to_universal import (
    convert_supervisely_3d_to_universal,
)
from universal_devkit.utils import read_json


def test_supervisely_3d_to_universal_single_file():
    # The path to the folder with a single file
    supervisely_annotations_path = get_relative_path(
        "assets/supervisely_annotations/single_file_input"
    )

    # The correct output for the single file
    correct_output_path = get_relative_path(
        "assets/supervisely_annotations/single_file_correct.pcd.json"
    )

    # The path to use as the output directory
    output_file_dir = get_relative_path(
        "assets/supervisely_annotations/single_file_output"
    )
    output_file_path = get_relative_path(
        "assets/supervisely_annotations/single_file_output/input.pcd.json"
    )

    # Convert the annotations
    convert_supervisely_3d_to_universal(supervisely_annotations_path, output_file_dir)

    # Make sure the output is correct
    correct_data = read_json(correct_output_path)
    output_annotations = read_json(output_file_path)

    ignore_keys = ["token", "sample_token", "instance_token"]

    assert len(correct_data) == len(output_annotations)

    for i in range(len(output_annotations)):
        output_d = output_annotations[i]
        correct_d = correct_data[i]
        assert equal_dicts(output_d, correct_d, ignore_keys=ignore_keys)

    shutil.rmtree(output_file_dir)
