# Algorithm:

1.  Ensure sweeps + sample directories are valid
2.  Get data on all the sensors:
    a. Get sensor token, channel, modality. -> sensor.json - You should have the ability to pass in an existing sensor json from another scene to make sure the same tokens are used

    b. Get sensor calibrations. -> calibrated_sensor.json

        Note that sensor.json and calibrated_sensor.json are kept seperate
        because when merging different scenes, you could have the same type of
        sensor (ex. CAMERA_FRONT) with a different calibration.

        Therefore, you want sensor.json to refer to a type of sensor (ex. LIDAR_TOP)
        and this should be re-used between different scenes.

3.  Get the vehicles pose throughout the scene. This should be provided as ego_pose.json.
    You will need to add tokens for every pose to uniquely identify them.

4.  Collect all sample data files.

    - First get data on all the sample files (this will be sample_data.json, but we
      don't have the sample_token yet).
    - Then use the primary sensor to decide what constitutes a sample.
    - Non-primary sensors should be matched to the nearest sample timestamp (using sample_token)
    - A non-primary sensor can have a many-to-one matching with the primary sensor.
      For instance, if a camera can take 8 pictures in the time for a full lidar scan to
      complete, the first 4 of those pictures should be matched with the nth - 1 scan
      and the remaining 4 of those pictures should be matched with the nth scan.
    - sample data paths should always be with respect to the scene directory as the root.
      Ex. `~/demo/samples/LIDAR_TOP/129172192.pcd` should be stored as `samples/LIDAR_TOP/129172192.pcd`
      This will make it easier to merge samples from different scenes

5.  Assign the nearest ego pose token to all sample data.

    - Each file should be matched individually to the nearest ego pose.
    - For instance, the 8 pictures mentioned earlier should all be matched to the closest
      ego pose, regardless of what the ego pose for the overall sample (as decided
      by the main sensor) is.

6.  Create a category.json and attribute.json

    - If these files already exist, they should be used

7.  Collect all data annotations for the primary sensor.

    - We are just using the primary sensor for annotations currently
    - In the future, we may add the ability to maintain annotations for non-main sensors
    - If an annotation has an annotation type that is not already in category.json, it should be added

8.  Identify annotations that exist across multiple timesteps.
    - The user will have the option to specify an instance_token for every annotation
    - If the user doesn't specify an instance_token, a new random one will be generated for each
      annotation (which means nothing will be tracked across frames).

### Example usage:

```
python3 universal_devkit/prepare_data/scene.py -i ~/data/universal-data-format-simple/input -o ~/data/universal-data-format-simple/output
```
