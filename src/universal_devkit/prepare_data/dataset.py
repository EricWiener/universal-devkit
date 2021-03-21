class Dataset:
    def __init__(self, scene_directory):
        """Create a dataset wrapper around a scene or multiple scenes

        Algorithm:
        1. Ensure all directories are correctly formatted universal-devkit scenes
        2. Create a Scene instance for each individual scene
        3. Merge the scenes. This will require:
            - merging sensor data with similar names
                (ex. all "LIDAR_TOP" should be grouped together)
            - merge together all JSON files
            - create a new scene.json
            - merge attributes and categories
            - merge all the sensor data: ex. all CAMERA_FRONT in each scene
                should be copied into a new merged/samples/CAMERA_FRONT


        Args:
            scene_directory (str): path to a directory containing universal-devkit
                formatted scenes
        """
        pass
