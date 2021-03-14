import shutil

from utils import equal_dicts, get_relative_path

from universal_devkit.scripts.ros_imu_pose import ros_imu_pose
from universal_devkit.utils import read_json


def test_imu_pose_single_file():
    IMU_pose_path = get_relative_path("assets/imu_pose/single_file_input.bag")

    # The correct output for the single file
    correct_output_path = get_relative_path("assets/imu_pose/single_file_correct.json")

    # The path to use as the output directory
    output_file_dir = get_relative_path("assets/imu_pose/single_file_output")
    output_file_path = get_relative_path("assets/imu_pose/single_file_output/IMU.json")

    topic = "/imu/data/raw"

    # Convert the annotations
    ros_imu_pose(IMU_pose_path, topic, output_file_dir)

    # Make sure the output is correct
    correct_data = read_json(correct_output_path)
    output_annotations = read_json(output_file_path)

    ignore_keys = []

    assert len(correct_data) == len(output_annotations)

    for i in range(len(output_annotations)):
        output_d = output_annotations[i]
        correct_d = correct_data[i]
        assert equal_dicts(output_d, correct_d, ignore_keys=ignore_keys)

    shutil.rmtree(output_file_dir)
