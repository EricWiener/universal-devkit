def get_instance_data(sample_annotation_data: list):
    """Gets a dictionary mapping every instance token -> data about it

    Args:
        sample_annotation_data (list): a list of dictionaries with
            sample annotation information

    Returns:
        dict: a dictionary mapping instance_tokens to dicts about them
    """
    # Map from instance_token -> dict
    instance_data = {}

    for annotation in sample_annotation_data:
        instance_token = annotation["instance_token"]

        if instance_token in instance_data:
            # If the instance token already exists in the instance_data
            timestamp = annotation["timestamp"]
            if timestamp < instance_data[instance_token]["first_annotation_timestamp"]:
                instance_data[instance_token]["first_annotation_token"] = annotation[
                    "token"
                ]
                instance_data[instance_token]["first_annotation_timestamp"] = timestamp
            elif timestamp > instance_data[instance_token]["last_annotation_timestamp"]:
                instance_data[instance_token]["last_annotation_token"] = annotation[
                    "token"
                ]
                instance_data[instance_token]["last_annotation_timestamp"] = timestamp

            # Update the count
            instance_data[instance_token]["nbr_annotations"] += 1

        else:
            # If we need to add the instance for the first time
            instance_data[instance_token] = {
                "token": instance_token,
                "category_token": annotation["category_token"],
                "nbr_annotations": 1,
                "first_annotation_token": annotation["token"],
                "first_annotation_timestamp": annotation["timestamp"],
                "last_annotation_token": annotation["token"],
                "last_annotation_timestamp": annotation["timestamp"],
            }

    # Remove timestamps
    for instance_dict in instance_data.values():
        del instance_dict["first_annotation_timestamp"]
        del instance_dict["last_annotation_timestamp"]

    return instance_data
