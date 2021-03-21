import os

from image_utils import get_image_dimensions

from universal_devkit.utils.utils import (
    create_token,
    get_all_non_hidden_files,
    get_file_extension,
    get_file_stem_name,
)


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
    files.remove("calibration.json")

    # Map from timestamp -> sample data
    # {
    #     "token": "ca9a282c9e77460f8360f564131a8af5",
    #     "timestamp": 1532402927647951,
    #     "prev": "",
    #     "next": "39586f9d59004284a7114a68825e8eec",
    #     "scene_token": "cc8c0bf57f984915a77078b10eb33198"
    # },
    sample_dict = {}

    # Get all the sample files (ignoring prev and next for now)
    for file in files:
        file_stem = get_file_stem_name(file)
        timestamp = int(file_stem)

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

    # Now add in prev and next
    timestamps = sample_dict.values()
    timestamps.sort()

    for i in range(1, len(timestamps) - 1):
        timestamp = timestamps[i]
        sample_dict[timestamp]["prev"] = timestamps[i - 1]
        sample_dict[timestamp]["next"] = timestamps[i + 1]

    # Handle special case of the first and the last
    sample_dict[timestamp[0]]["next"] = timestamps[1]
    sample_dict[timestamp[-1]]["prev"] = timestamps[-2]

    return sample_dict, timestamps


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

    if modality == "camera":
        data = {**data, **get_data_from_img(file_path)}

    return data


def get_data_from_pcd(file_path, is_radar=False):
    pass


def get_data_from_img(file_path):
    image_width, image_height = get_image_dimensions(file_path)
    return {"height": image_height, "width": image_width}
