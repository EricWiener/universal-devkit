import argparse
import os

from ego_pose import get_ego_pose_data
from instance import get_instance_data
from sample import get_file_data, get_sample_json
from sample_annotation import get_sample_annotation
from sensor import get_sensor_calibration, get_sensor_json
from utils import (
    create_token,
    get_all_non_hidden_files,
    get_closest_match,
    get_file_stem_name,
)


class Scene:
    def __init__(
        self,
        input_directory,
        scene_token,
        sensor_json_path=None,
        primary_sensor="LIDAR_TOP",
    ):
        """Generates data for a single scene

        Expected file structure::

            single-scene
            ├── map.png
            ├── log.txt
            ├── ego_pose.json
            ├── samples
            │   ├── CAM_BACK
            |   │   └── calibration.json
            │   ├── CAM_BACK_LEFT
            |   │   └── calibration.json
            │   ├── CAM_BACK_RIGHT
            |   │   └── calibration.json
            │   ├── CAM_FRONT
            |   │   └── calibration.json
            │   ├── CAM_FRONT_LEFT
            |   │   └── calibration.json
            │   ├── CAM_FRONT_RIGHT
            |   │   └── calibration.json
            │   ├── LIDAR_TOP
            |   │   └── calibration.json
            │   ├── RADAR_BACK_LEFT
            |   │   └── calibration.json
            │   ├── RADAR_BACK_RIGHT
            |   │   └── calibration.json
            │   ├── RADAR_FRONT
            |   │   └── calibration.json
            │   ├── RADAR_FRONT_LEFT
            |   │   └── calibration.json
            │   └── RADAR_FRONT_RIGHT
            |       └── calibration.json
            ├── sweeps
            │   ├── CAM_BACK
            │   ├── CAM_BACK_LEFT
            │   ├── CAM_BACK_RIGHT
            │   ├── CAM_FRONT
            │   ├── CAM_FRONT_LEFT
            │   ├── CAM_FRONT_RIGHT
            │   ├── LIDAR_TOP
            │   ├── RADAR_BACK_LEFT
            │   ├── RADAR_BACK_RIGHT
            │   ├── RADAR_FRONT
            │   ├── RADAR_FRONT_LEFT
            │   └── RADAR_FRONT_RIGHT
            └── single-scene

        Args:
            input_directory (str): input directory path
        """
        self.SWEEP_DIR_PATH = os.path.join(input_directory, "sweeps")
        self.SAMPLE_DIR_PATH = os.path.join(input_directory, "samples")
        self.SCENE_TOKEN = scene_token if scene_token else create_token()

        assert os.path.exists(self.SWEEP_DIR_PATH), "Unable to locate sweeps directory"
        assert os.path.exists(self.SAMPLE_DIR_PATH), "Unable to locate sample directory"

        # The sensor tokens should remain the same for different scenes
        # Dictionary mapping sensor channel -> sensor info
        # Ex: "CAM_FRONT_RIGHT" -> {
        #   "token": "2f7ad058f1ac5557bf321c7543758f43",
        #   "channel": "CAM_FRONT_RIGHT",
        #   "modality": "camera"
        # }
        self.SENSOR_JSON_DICT = get_sensor_json(
            self.SAMPLE_DIR_PATH, sensor_json_path=sensor_json_path
        )

        # The calibration tokens for a sensor can change for different scenes
        # Dictionary mapping sensor channel -> calibration data
        # "CAM_FRONT_RIGHT" -> {
        #     // changes for a specific sensor per scene
        #     "token": "f4d2a6c281f34a7eb8bb033d82321f79",
        #     // same for a specific sensor
        #     "sensor_token": "47fcd48f71d75e0da5c8c1704a9bfe0a",
        #     "translation": [...],
        #     "rotation": [...],
        #     "camera_intrinsic": [...] // optional
        # },
        self.SENSOR_CALIBRATION_DICT = get_sensor_calibration(
            self.SAMPLE_DIR_PATH, self.SENSOR_JSON_DICT
        )

        # Get ego pose data
        # self.EGO_POSE_DICT maps timestamps -> ego pose dicts
        ego_pose_path = os.path.join(input_directory, "ego_pose.json")
        assert os.path.exists(ego_pose_path), "Unable to locate ego_pose.json"
        self.EGO_POSE_DICT, self.EGO_POSE_TIMESTAMPS = get_ego_pose_data(ego_pose_path)

        # Get the sample data mapping timestamps -> sample data
        # 1532402927647951 -> {
        #   "token": "ca9a282c9e77460f8360f564131a8af5",
        #   "timestamp": 1532402927647951,
        #   "prev": "",
        #   "next": "39586f9d59004284a7114a68825e8eec",
        #   "scene_token": "cc8c0bf57f984915a77078b10eb33198"
        # },
        self.SAMPLE_DICT, self.SAMPLE_TIMESTAMPS = get_sample_json(
            self.SAMPLE_DIR_PATH, self.scene_token, primary_sensor=primary_sensor
        )

        sample_data_keyframes_dict = self.get_sample_data(self.SAMPLE_DIR_PATH, True)
        sample_data_sweeps_dict = self.get_sample_data(self.SWEEP_DIR_PATH, False)
        self.SAMPLE_DATA_DICT = {
            **sample_data_keyframes_dict,
            **sample_data_sweeps_dict,
        }

        # Get the sample annotations (a list of dictionaries with all the annotations)
        self.SAMPLE_ANNOTATIONS = get_sample_annotation(
            input_directory, self.SAMPLE_DATA_DICT
        )

        # Get the instance data (a list of dictionaries with each instance of an object)
        # This should be <= the size of self.SAMPLE_ANNOTATIONS
        self.INSTANCE_DATA_DICT = get_instance_data(self.SAMPLE_ANNOTATIONS)

    def get_sample_data(self, directory_path: str, is_key_frame: bool):
        # Dictionary of annotation_token -> annotation dict
        annotations = {}

        for sensor in self.SENSOR_CALIBRATION_DICT:
            sensor_dir = os.path.join(directory_path)
            calibrated_sensor_token = self.SENSOR_CALIBRATION_DICT[sensor]["token"]

            # Store a dict with per sensor annotations to use for specifying
            # the prev and next tokens
            # timestamp -> annotation token
            sensor_annotations = {}

            files = get_all_non_hidden_files(sensor_dir)

            for file in files:
                file_stem = get_file_stem_name(file)
                timestamp = int(file_stem)

                # @TODO: this should be the full file path being passed
                # not the file name
                annotation = self.get_sample_data_for_file(
                    file, timestamp, calibrated_sensor_token, is_key_frame
                )
                annotations[annotation["token"]] = annotation
                sensor_annotations[timestamp] = annotation["token"]

            # Add prev and next
            timestamps = sensor_annotations.keys()
            timestamps.sort()

            for i in range(1, len(timestamps) - 1):
                timestamp = timestamps[i]
                ann_token = sensor_annotations[timestamp]
                annotations[ann_token]["prev"] = sensor_annotations[timestamps[i - 1]]
                annotations[ann_token]["next"] = sensor_annotations[timestamps[i + 1]]

            # Handle the first and last
            first_ann_token = sensor_annotations[timestamps[0]]
            annotations[first_ann_token]["next"] = sensor_annotations[timestamps[1]]

            last_ann_token = sensor_annotations[timestamps[-1]]
            annotations[last_ann_token]["prev"] = sensor_annotations[timestamps[-2]]

        return annotations

    def get_sample_data_for_file(
        self, file_path, timestamp, calibrated_sensor_token, is_key_frame
    ):
        # Get the sample token
        closest_sample_timestamp = get_closest_match(self.SAMPLE_TIMESTAMPS, timestamp)
        sample_token = self.SAMPLE_DICT[closest_sample_timestamp]["token"]

        # Get the ego token
        closest_ego_timestamp = get_closest_match(self.EGO_POSE_TIMESTAMPS, timestamp)
        ego_token = self.EGO_POSE_DICT[closest_ego_timestamp]["token"]

        annotation = {
            "token": create_token(),
            "sample_token": sample_token,
            "ego_pose_token": ego_token,
            "calibrated_sensor_token": calibrated_sensor_token,
            "timestamp": timestamp,
            "is_key_frame": is_key_frame,
            # @TODO: this should be relative to the data directory
            "filename": file_path,
            "prev": "",
            "next": "",
        }

        # @TODO: this should be the full file path being passed
        # not the file name
        annotation = {**annotation, **get_file_data(file_path)}

        return annotation


def main():
    pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", type=str, help="The path to the input directory")
    ap.add_argument("-o", "--output", type=str, help="The path to the output directory")
    args = vars(ap.parse_args())
    main(args["input"], args["output"])
