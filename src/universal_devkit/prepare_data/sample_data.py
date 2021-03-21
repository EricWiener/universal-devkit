import os

from constants import Constants
from ego_pose import EgoPoseData
from image_utils import get_image_dimensions
from sample import Sample

from universal_devkit.utils.utils import (
    add_prev_next_to_list_of_dicts,
    create_token,
    get_all_non_hidden_files,
    get_file_extension,
    get_timestamp_from_file_path,
)


class SampleData:
    def __init__(self, ego_pose_data: EgoPoseData, sample: Sample):
        self.sensors_to_data = {}
        self.ego_pose_data = EgoPoseData
        self.sample = Sample

    def get_sample_data(self, directory_path: str, is_key_frame: bool):
        """Gets a dictionary with information on each of the samples

        Args:
            directory_path (str): sample directory
            is_key_frame (bool): whether the frame is a keyframe

        Returns:
            tuple(dict, list): a dictionary of timestamps -> sample dicts,
                a list of sorted timestamps
        """

        """
        Dictionary mapping sensor name to corresponding data files.

        Of form:
        ```
        sample data token -> {
            "token": XXXXXX,
            "sample_token": sample_token,
            "ego_pose_token": ego_token,
            "calibrated_sensor_token": calibrated_sensor_token,
            "timestamp": timestamp,
            "is_key_frame": is_key_frame,
            "filename": file_path,
            "prev": "",
            "next": "",
        }
        ```
        """
        token_to_sample_data = {}

        # @TODO: need to combine both sweeps and samples when calculating "prev"
        # and "next" values.

        for sensor in self.SENSOR_CALIBRATION_DICT:
            sensor_dir = os.path.join(directory_path, sensor)
            calibrated_sensor_token = self.SENSOR_CALIBRATION_DICT[sensor]["token"]

            # Store a dict with per sensor annotations to use for specifying
            # the prev and next tokens
            # timestamp -> sample data object (just for one sensor)
            timestamp_to_sample_data = {}

            files = get_all_non_hidden_files(
                sensor_dir, exclude=[Constants.sensor_calibration_file_name]
            )

            if len(files) < 2:
                # Require at least 2 timestamps
                print(
                    "Not enough data for sensor: {}. Skipping".format(
                        self.primary_sensor
                    )
                )
                return {}, []

            for file in files:
                timestamp = get_timestamp_from_file_path(file)

                # Assign annotation to a temporary variable vs. directly
                # into an object to allow updates to the annotation to
                # be seen in both dictionaries

                # @TODO: this should be the full file path being passed
                # not the file name
                sample_data_for_file = self.get_sample_data_for_file(
                    file, timestamp, calibrated_sensor_token, is_key_frame
                )
                token_to_sample_data[
                    sample_data_for_file["token"]
                ] = sample_data_for_file
                timestamp_to_sample_data[timestamp] = sample_data_for_file

            # Add prev and next tokens to sample data for this sensor
            timestamp_to_sample_data, timestamps = add_prev_next_to_list_of_dicts(
                timestamp_to_sample_data
            )

        return token_to_sample_data

    def get_sample_data_for_file(
        self, file_path, timestamp, calibrated_sensor_token, is_key_frame
    ):
        # Get the sample token
        sample_token = self.sample.get_closest_sample_token(timestamp)

        # Get the ego token
        ego_token = self.ego_pose_data.get_closest_pose_token(timestamp)

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


def get_file_data(file_path, modality: str):
    """Gets data on a single data file

    Args:
        file_path (str): path to the data file
        modality (str): the modality "camera", "lidar", "radar"

    Returns:
        dict: dictionary describing data on the file
    """
    file_extension = get_file_extension(file_path)

    data = {
        "fileformat": file_extension,
        "height": 0,
        "width": 0,
    }

    if modality == Constants.modality_camera:
        data = {**data, **get_data_from_img(file_path)}
    elif modality == Constants.modality_lidar:
        data = {**data, **get_data_from_pcd(file_path)}
    elif modality == Constants.modality_radar:
        data = {**data, **get_data_from_pcd(file_path, is_radar=True)}

    return data


def get_data_from_pcd(file_path, is_radar=False):
    # @TODO: write this function
    return {}


def get_data_from_img(file_path):
    image_width, image_height = get_image_dimensions(file_path)
    return {"height": image_height, "width": image_width}
