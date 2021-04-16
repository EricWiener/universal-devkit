from utils import get_relative_path

from universal_devkit.utils.utils import (
    get_all_non_hidden_files,
    get_closest_match,
    get_timestamp,
)


def test_get_timestamp():
    example_imu_reading_1 = {"header": {"stamp": {"secs": 100, "nsecs": 150}}}
    assert get_timestamp(example_imu_reading_1) == "100000000150"

    example_imu_reading_2 = {"header": {"stamp": {"secs": 1, "nsecs": 0}}}
    assert get_timestamp(example_imu_reading_2) == "1000000000"

    example_imu_reading_3 = {"header": {"stamp": {"secs": 0, "nsecs": 0}}}
    assert get_timestamp(example_imu_reading_3) == "0"


def test_get_all_non_hidden_files():

    test_directory = get_relative_path("assets/test_get_all_non_hidden_files")

    test1 = ["test1.txt"]
    test2 = ["test1.txt", "test2.txt"]

    test1_correct = ["test2.txt", "test3.txt", "test4.txt"]
    test2_correct = ["test3.txt", "test4.txt"]
    test3_correct = ["test1.txt", "test2.txt", "test3.txt", "test4.txt"]

    print(get_all_non_hidden_files(test_directory, test1))

    assert get_all_non_hidden_files(test_directory, test1) == test1_correct
    assert get_all_non_hidden_files(test_directory, test2) == test2_correct
    assert get_all_non_hidden_files(test_directory) == test3_correct


def test_get_closest_match():

    # Test 1
    test = [0, 2, 3, 5, 6, 10, 14, 30]
    assert get_closest_match(test, 7) == 6

    # Test 2
    assert get_closest_match(test, 8) == 6

    # Test 3
    assert get_closest_match(test, 1) == 0

    # Test 4:
    assert get_closest_match(test, 30) == 30


if __name__ == "__main__":
    test_get_all_non_hidden_files()
