from utils import create_token, get_full_path_to_file, read_json


def get_sample_annotation(root_data_dir: str, sample_dict: dict):
    full_path = get_full_path_to_file(root_data_dir, sample_dict["filepath"])
    sample_token = sample_dict["token"]

    sample_annotation_data = read_json(full_path)

    # A list of dictionaries where each dict is a sample annotation
    annotations = []

    # Loop through all the annotations for a specific file
    for ann in sample_annotation_data:
        # @TODO: the user needs to add a "category_token" key
        annotation = {
            "token": create_token(),
            "sample_token": sample_token,
            # @TODO: need to actually add in tracking over time
            "instance_token": create_token(),
            # @TODO: need to add in correct visibility token
            "visibility_token": "4",
            "attribute_tokens": [],
            "prev": "",
            "next": "",
            # @TODO: use bbox-utils to actually get the correct number of lidar
            # pts if this is a PCD File
            "num_lidar_pts": 0,
            "num_radar_pts": 0,
        }

        # Append all the attributes from the annotation file
        # Any instance_token specified by the user will override the randomly
        # generated one
        annotation = {**annotation, **ann}

        # @TODO: add in data formatting checking

        annotations.append(annotation)

    return annotations
