import os

from utils import (
    convert_list_to_dict,
    create_token,
    get_immediate_directories,
    read_json,
)


def get_sensor_json(self, sample_dir_path, sensor_json_path=None):
    sensor_data = {}

    if sensor_json_path:
        sensor_list = read_json(sensor_json_path)
        sensor_data = convert_list_to_dict(sensor_list)

    sensors = get_immediate_directories(sample_dir_path)

    # sensor_channel will be something like "LIDAR_TOP", "RADAR_FRONT_RIGHT", etc.
    for sensor_channel in sensors:
        if sensor_channel not in sensor_data:
            # If the sensor doesn't exist already, we will create it
            sensor_info = {
                "token": create_token(),
                "channel": sensor_channel,
                "modality": get_modality_from_name(sensor_channel),
            }
            sensor_data[sensor_channel] = sensor_info

    return sensor_data


def get_sensor_calibration(self, sample_dir_path, sensor_json_dict):
    calibration_dict = {}

    # sensor_channel will be something like "LIDAR_TOP", "RADAR_FRONT_RIGHT", etc.
    for sensor_channel in sensor_json_dict:
        calib_file = os.path.join(sample_dir_path, sensor_channel, "calibration.json")

        if not os.path.exists(calib_file):
            print(
                "Unable to find calibration file for {}. Skipping".format(
                    sensor_channel
                )
            )
            continue

        calib_data = read_json(calib_file)
        calibration_dict[sensor_channel] = calib_data
        calibration_dict[sensor_channel]["token"] = create_token()
        calibration_dict[sensor_channel]["sensor_token"] = sensor_json_dict[
            sensor_channel
        ]["token"]

    return calibration_dict


def get_modality_from_name(sensor_name: str):
    """Gets the modality of a sensor from its name.

    Args:
        sensor_name (str): the name of the sensor. Ex: CAM_FRONT_RIGHT, LIDAR_TOP, etc.

    Returns:
        str: the sensor modality
    """
    if "CAM" in sensor_name:
        return "camera"
    elif "RADAR" in sensor_name:
        return "radar"
    elif "LIDAR" in sensor_name:
        return "lidar"
    else:
        return "unknown"
