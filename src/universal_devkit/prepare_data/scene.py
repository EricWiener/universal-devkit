import argparse
import os

from ego_pose import EgoPoseData
from instance import get_instance_data
from sample import Sample
from sample_annotation import get_sample_annotation
from sample_data import SampleData
from sensor import get_sensor_calibration, get_sensor_json

from universal_devkit.utils.utils import create_token


class Scene:
    def __init__(
        self,
        input_directory,
        scene_token=None,
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
        self.primary_sensor = primary_sensor

        assert os.path.exists(self.SWEEP_DIR_PATH), "Unable to locate sweeps directory"
        assert os.path.exists(self.SAMPLE_DIR_PATH), "Unable to locate sample directory"

        """
        The sensor tokens should remain the same for different scenes
        Dictionary mapping sensor channel -> sensor info

        Ex:
        ```
        "CAM_FRONT_RIGHT" -> {
            "token": "2f7ad058f1ac5557bf321c7543758f43",
            "channel": "CAM_FRONT_RIGHT",
            "modality": "camera"
        }
        ```
        """
        self.SENSOR_JSON_DICT = get_sensor_json(
            self.SAMPLE_DIR_PATH, sensor_json_path=sensor_json_path
        )

        """
        The calibration tokens for a sensor can change for different scenes
        Dictionary mapping sensor channel -> calibration data

        ```
        "CAM_FRONT_RIGHT" -> {
            // changes for a specific sensor per scene
            "token": "f4d2a6c281f34a7eb8bb033d82321f79",
            // same for a specific sensor
            "sensor_token": "47fcd48f71d75e0da5c8c1704a9bfe0a",
            "translation": [...],
            "rotation": [...],
            "camera_intrinsic": [...] // optional
        },
        ```
        """
        self.SENSOR_CALIBRATION_DICT = get_sensor_calibration(
            self.SAMPLE_DIR_PATH, self.SENSOR_JSON_DICT
        )

        # Get ego pose data
        # self.EGO_POSE_DICT maps timestamps -> ego pose dicts
        ego_pose_path = os.path.join(input_directory, "ego_pose.json")
        assert os.path.exists(ego_pose_path), "Unable to locate ego_pose.json"
        self.ego_pose_data = EgoPoseData(ego_pose_path)

        """
        Get info on each sample mapping timestamps -> sample data

        This uses the timestamps of the primary sensor when deciding
        the timestamps of each sample.

        ```
        1532402927647951 -> {
            "token": "ca9a282c9e77460f8360f564131a8af5",
            "timestamp": 1532402927647951,
            "prev": "",
            "next": "39586f9d59004284a7114a68825e8eec",
            "scene_token": "cc8c0bf57f984915a77078b10eb33198"
        },
        ```
        """
        self.sample = Sample(
            self.SAMPLE_DIR_PATH, self.SCENE_TOKEN, primary_sensor=primary_sensor
        )

        self.sample_data = SampleData(self.ego_pose_data, self.sample)

        # These dictionaries map sample_data_token -> dictionary on that sample file
        sample_data_keyframes_dict = self.sample_data.get_sample_data(
            self.SAMPLE_DIR_PATH, True
        )
        sample_data_sweeps_dict = self.sample_data.get_sample_data(
            self.SWEEP_DIR_PATH, False
        )
        self.SAMPLE_DATA_DICT = {
            **sample_data_keyframes_dict,
            **sample_data_sweeps_dict,
        }

        # Get the sample annotations (a list of dictionaries with all the annotations)
        # for each annotation file in self.SAMPLE_DATA_DICT
        self.SAMPLE_ANNOTATIONS = []
        for sample_data_token in self.SAMPLE_DATA_DICT:
            sample_annotations = get_sample_annotation(
                input_directory,
                self.SAMPLE_DATA_DICT[sample_data_token],
            )
            self.SAMPLE_ANNOTATIONS.append(sample_annotations)

        # Get the instance data (a list of dictionaries with each instance of an object)
        # This should be <= the size of self.SAMPLE_ANNOTATIONS
        self.INSTANCE_DATA_DICT = get_instance_data(self.SAMPLE_ANNOTATIONS)


def main(input_directory, output_directory):
    _ = Scene(input_directory)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--input", type=str, required=True, help="The path to the input directory"
    )
    ap.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="The path to the output directory",
    )
    args = vars(ap.parse_args())
    main(args["input"], args["output"])
