class Constants:
    # This is a single file with all calibrated sensors
    # information produced by the devkit
    sensor_calibration_file_name = "calibrated_sensor.json"

    # When a user gives input data, each sensor should have a
    # calibration.json file inside every sample sensor's directory
    per_sensor_input_calibration_file_name = "calibration.json"

    modality_lidar = "lidar"
    modality_camera = "camera"
    modality_radar = "radar"
    modality_hydrophone = "hydrophone"
