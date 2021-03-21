from universal_devkit.utils.utils import (
    convert_list_to_dict,
    create_token,
    get_closest_match,
    read_json,
)


class EgoPoseData:
    def __init__(self, ego_pose_json_path):
        self.timestamps_to_pose, self.timestamps = get_ego_pose_data(ego_pose_json_path)

    def get_closest_pose_token(self, timestamp):
        """Gets the closest ego pose for a certain timestamp

        Args:
            timestamp (int): the timestamp in nanoseconds

        Returns:
            str: the UUID token for the closest ego pose
        """
        closest_ego_timestamp = get_closest_match(self.timestamps, timestamp)
        ego_token = self.timestamps_to_pose[closest_ego_timestamp]["token"]

        return ego_token


def validate_ego_pose(ego_pose_list):
    """Validates Ego Pose data is correctly formatted.

    Should receive a list of form::

        [
            {
                "timestamp": 1532402927814384,
                "rotation": [
                    0.5731787718287827,
                    -0.0015811634307974854,
                    0.013859363182046986,
                    -0.8193116095230444
                ],
                "translation": [
                    410.77878632230204,
                    1179.4673290964536,
                    0.0
                ]
            },
            ...
        ]

    Args:
        ego_pose_list ([type]): [description]
    """
    for ego_pose in ego_pose_list:
        # Check timestamp
        assert "timestamp" in ego_pose, "Ego Pose missing timestamp"
        assert isinstance(
            ego_pose["timestamp"], int
        ), "Ego Pose should be an int. Received {}".format(type(ego_pose["timestamp"]))

        # Check rotation
        assert "rotation" in ego_pose, "Ego Pose missing rotation"
        assert (
            len(ego_pose["rotation"]) == 4
        ), "Ego Pose rotation should be an array of length 4"

        # Check translation
        assert "translation" in ego_pose, "Ego Pose missing translation"
        assert (
            len(ego_pose["translation"]) == 3
        ), "Ego Pose translation should be an array of length 3"


def get_ego_pose_data(ego_pose_json_path):
    """Reads a list of ego pose data from a JSON file and adds unique tokens

    Args:
        ego_pose_json_path (str): path to the ego pose data

    Returns:
        tuple(dict, list): a dictionary mapping timestamps -> pose dicts,
        a list of sorted ego pose timestamps
    """
    ego_pose_list = read_json(ego_pose_json_path)
    validate_ego_pose(ego_pose_list)

    # Add unique tokens to each entry in the list
    for pose in ego_pose_list:
        pose["token"] = create_token()

    ego_pose_dict = convert_list_to_dict(ego_pose_list, using_key="timestamp")
    ego_pose_timestamps = list(ego_pose_dict.keys())
    ego_pose_timestamps.sort()

    return ego_pose_dict, ego_pose_timestamps
