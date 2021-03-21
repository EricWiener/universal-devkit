import os

from constants import Constants

from universal_devkit.utils.utils import (
    add_prev_next_to_list_of_dicts,
    create_token,
    get_all_non_hidden_files,
    get_closest_match,
    get_timestamp_from_file_path,
)


class Sample:
    def __init__(self, sample_dir_path, scene_token, primary_sensor="LIDAR_TOP"):
        self.timestamps_to_sample, self.timestamps = get_sample_json(
            sample_dir_path, scene_token, primary_sensor="LIDAR_TOP"
        )

    def get_closest_sample_token(self, timestamp):
        """Gets the closest sample token for a certain timestamp

        Args:
            timestamp (int): the timestamp in nanoseconds

        Returns:
            str: the UUID token for the closest sample
        """
        closest_sample_timestamp = get_closest_match(self.timestamps, timestamp)
        sample_token = self.timestamps_to_sample[closest_sample_timestamp]["token"]

        return sample_token


def get_sample_json(sample_dir_path, scene_token, primary_sensor="LIDAR_TOP"):
    """Gets a dictionary with information on each of the samples

    Args:
        sample_dir_path (str): sample directory
        scene_token (str): the token identifying the scene
        primary_sensor (str, optional): the sensor to use to decide timestamps.
            Defaults to "LIDAR_TOP".

    Returns:
        tuple(dict, list): a dictionary of timestamps -> sample dicts,
            a list of sorted timestamps
    """
    sensor_data_dir = os.path.join(sample_dir_path, primary_sensor)

    files = get_all_non_hidden_files(sensor_data_dir)

    # Remove calibration file
    files.remove(Constants.per_sensor_input_calibration_file_name)

    """
    Map from timestamp -> sample data

    Ex:
    ```
    {
        "token": "ca9a282c9e77460f8360f564131a8af5",
        "timestamp": 1532402927647951,
        "prev": "",
        "next": "39586f9d59004284a7114a68825e8eec",
        "scene_token": "cc8c0bf57f984915a77078b10eb33198"
    },
    ```
    """
    sample_dict = {}

    # Get all the sample files (ignoring prev and next for now)
    for file in files:
        timestamp = get_timestamp_from_file_path(file)

        assert timestamp not in sample_dict, "Duplicate timestamp found {}".format(
            timestamp
        )

        sample_dict[timestamp] = {
            "token": create_token(),
            "timestamp": timestamp,
            "scene_token": scene_token,
            "prev": "",
            "next": "",
        }

    sample_dict, timestamps = add_prev_next_to_list_of_dicts(sample_dict)

    return sample_dict, timestamps
