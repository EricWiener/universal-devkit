import uuid
from pathlib import Path
import os
from .utils import read_json, get_existing_token, remove_key_from_dicts


def validate_calibration_data(data):
    """Validates whether the calibration data is correct

    Args:
        data (dict): dictionary with sensor calibration data

    Returns:
        bool: whether the data is valid or not.
    """
    # @TODO: complete this function
    return True


def get_calibration_data(sensor_path):
    get_calib_path = lambda sensor_path: os.path.join(
        sensor_path, "calibrated_sensor.json"
    )

    data = read_json(get_calib_path(sensor_path))

    assert validate_calibration_data(data), "Calibration data invalid: {}".format(
        sensor_path
    )

    return data


def get_sensor_calibrations(sample_dir, sensor_json_path):
    sensor_calibrations = []

    # Loop through all directories (camera folders) in the sample directory
    # and get the calibration data for them
    sample_dir_path = Path(sample_dir)
    for f in sample_dir_path.iterdir():
        if f.is_dir():
            calib_data = get_calibration_data(f.path)

            # Add the channel name for use in getting sensor keys
            calib_data["channel"] = f.name
            sensor_calibrations.append()

    # Get sensor keys for all the calibrations
    sensor_calibrations = get_existing_token(
        sensor_calibrations, sensor_json_path, "channel", "sensor_token"
    )

    # Remove the channel property
    remove_key_from_dicts(sensor_calibrations, "channel")

    return sensor_calibrations