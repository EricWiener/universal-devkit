import numpy as np

from universal_devkit.scripts.calculate_extrinsic_matrix import (
    euler_angle_to_rotation_matrix,
    extrinsic_to_static_transform,
    static_transform_to_extrinsic,
)


def test_euler_angle_to_rotation_matrix():
    _, _, _, yaw, pitch, roll = [0.5080, 0.0, 0.1778, 0, 0.05, 0]
    rotation = euler_angle_to_rotation_matrix([yaw, pitch, roll])
    correct_rotation = np.array(
        [
            [0.99875026, 0.0, 0.04997917],
            [
                0.0,
                1.0,
                0.0,
            ],
            [-0.04997917, 0.0, 0.99875026],
        ]
    )
    assert np.allclose(rotation, correct_rotation)


def test_extrinsic_to_static_transform():
    camera_to_base_static = np.array([0.5080, 0.0, 0.1778, 0, 0.05, 0])
    camera_to_base_extrinsic = static_transform_to_extrinsic(camera_to_base_static)

    resulting_static = extrinsic_to_static_transform(camera_to_base_extrinsic)
    assert np.allclose(resulting_static, camera_to_base_static)


def test_static_transform_to_extrinsic():
    camera_to_base_static = np.array([0.5080, 0.0, 0.1778, 0, 0.05, 0])
    camera_to_base = static_transform_to_extrinsic(camera_to_base_static)
    correct_extrinsic = np.array(
        [
            [0.99875026, 0.0, 0.04997917, 0.508],
            [0.0, 1.0, 0.0, 0.0],
            [
                -0.04997917,
                0.0,
                0.99875026,
                0.1778,
            ],
            [
                0.0,
                0.0,
                0.0,
                1.0,
            ],
        ]
    )
    assert np.allclose(camera_to_base, correct_extrinsic)
