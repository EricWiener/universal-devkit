import argparse
import os
from pathlib import Path

from constants import Constants

from universal_devkit.utils.utils import write_json

from .get_sensors import get_sensor_calibrations


def main(data_path, out_path):
    """Formats data to be used by the UMA devkit

    Args:
        data_path (str): the path to the data folder
        out_path (str): the path to save resulting formatted data
    """

    # Create the output directories
    SCENE_NAME = Path(out_path).name
    OUT_SWEEP_DIR_PATH = os.path.join(out_path, "sweeps")
    OUT_SAMPLE_DIR_PATH = os.path.join(out_path, "samples")
    OUT_LOG_DIR_PATH = os.path.join(out_path, "logs")
    OUT_JSON_DIR_PATH = os.path.join(out_path, SCENE_NAME)
    Path(out_path).mkdir(parents=True, exist_ok=True)
    Path(OUT_SWEEP_DIR_PATH).mkdir(parents=True, exist_ok=True)
    Path(OUT_SAMPLE_DIR_PATH).mkdir(parents=True, exist_ok=True)
    Path(OUT_LOG_DIR_PATH).mkdir(parents=True, exist_ok=True)
    Path(OUT_JSON_DIR_PATH).mkdir(parents=True, exist_ok=True)

    # Get paths to input data
    # ATTRIBUTE_PATH = os.path.join(data_path, "attribute.json")
    # CATEGORY_PATH = os.path.join(data_path, "category.json")
    # VISIBILITY_PATH = os.path.join(data_path, "visibility.json")
    SENSOR_PATH = os.path.join(data_path, "sensor.json")
    # LOG_DIR_PATH = os.path.join(data_path, "logs")
    SAMPLES_DIR_PATH = os.path.join(data_path, "samples")
    # SWEEPS_DIR_PATH = os.path.join(data_path, "sweeps")

    # Create paths to output data
    CALIBRATION_DATA = os.path.join(
        OUT_JSON_DIR_PATH, Constants.sensor_calibration_file_name
    )

    # Get the sensor calibration
    calibration_data = get_sensor_calibrations(SAMPLES_DIR_PATH, SENSOR_PATH)
    write_json(calibration_data, CALIBRATION_DATA)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", type=str, help="The path to the input directory")
    ap.add_argument("-o", "--output", type=str, help="The path to the output directory")
    args = vars(ap.parse_args())
    main(args["input"], args["output"])
