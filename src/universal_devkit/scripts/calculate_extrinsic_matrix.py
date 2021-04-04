import math

import numpy as np


# Calculates Rotation Matrix given euler angles.
def euler_angle_to_rotation_matrix(theta):
    """
    Converts from theta [yaw, pitch, roll] to a rotation matrix
    """

    R_x = np.array(
        [
            [1, 0, 0],
            [0, math.cos(theta[0]), -math.sin(theta[0])],
            [0, math.sin(theta[0]), math.cos(theta[0])],
        ]
    )

    R_y = np.array(
        [
            [math.cos(theta[1]), 0, math.sin(theta[1])],
            [0, 1, 0],
            [-math.sin(theta[1]), 0, math.cos(theta[1])],
        ]
    )

    R_z = np.array(
        [
            [math.cos(theta[2]), -math.sin(theta[2]), 0],
            [math.sin(theta[2]), math.cos(theta[2]), 0],
            [0, 0, 1],
        ]
    )

    R = np.dot(R_z, np.dot(R_y, R_x))

    return R


def rotation_matrix_to_euler_angle(R):
    """
    Converts a rotation matrix to [yaw, pitch, roll]
    """
    yaw = math.atan2(R[1, 0], R[0, 0])
    pitch = math.atan2(-R[2, 0], math.sqrt(R[2, 1] ** 2 + R[2, 2] ** 2))
    roll = math.atan2(R[2, 1], R[2, 2])

    return yaw, pitch, roll


def static_transform_to_extrinsic(transform):
    """
    Calculates the extrinsic matrix for a ROS static_transform_publisher

    Parameters:
    - transform: a list with [x, y, z yaw, pitch, roll]
    """
    assert len(transform) == 6

    x, y, z, yaw, pitch, roll = transform
    rotation = euler_angle_to_rotation_matrix([yaw, pitch, roll])
    translation = np.array([x, y, z]).reshape(-1, 1)
    homogeneous = get_homogeneous_transformation(rotation, translation)
    return homogeneous


def extrinsic_to_static_transform(mat):
    """Converts an extrinsic matrix into rotational and translational components.

    Args:
        mat (np.array): a 4x4 extrinsic matrix

    Returns:
        np.array: a 1x6 np.array of form x, y, z, yaw, pitch, roll
    """
    x, y, z = mat[:3, 3]
    yaw, pitch, roll = rotation_matrix_to_euler_angle(mat)

    return np.array([x, y, z, yaw, pitch, roll])


def get_homogeneous_transformation(rotation, translation):
    """
    Parameters:
    - rotation: a 3x3 rotation np array
    - translation: a 3x1 translation np array
    """
    homogeneous = np.zeros((4, 4))
    homogeneous[-1][-1] = 1
    homogeneous[:3, :3] = rotation
    homogeneous[:3, -1:] = translation
    return homogeneous


def get_relative_transformation(a_to_base, b_to_base):
    """
    Finds the relative transformation from a to b given transformations for both
    relative to base_link.

    See: https://stackoverflow.com/a/55169091/6942666 for more details

    Parameters:
    - a_to_base: 4x4 np.array representing homoegenous transformation of a to base_link
    - b_to_base: 4x4 np.array representing homoegenous transformation of b to base_link
    """

    base_to_a = np.linalg.inv(a_to_base)
    return base_to_a @ b_to_base


if __name__ == "__main__":
    """
    <node pkg="tf" type="static_transform_publisher"
        respawn="true"
        name="camera_static_transform_publisher"
        args="0.5080 0.0 0.1778 0 0.05 0 base_link camera 100"
    />

    <node pkg="tf" type="static_transform_publisher"
        respawn="true"
        name="velodyne_static_transform_publisher"
        args="0.4445 0.0 0.09525 0.0 0.06981 0.0 base_link velodyne 100"
    />

    Camera static transform:
    [[ 0.99875026  0.          0.04997917  0.508     ]
    [ 0.          1.          0.          0.        ]
    [-0.04997917  0.          0.99875026  0.1778    ]
    [ 0.          0.          0.          1.        ]]

    Velodyne static transform:
    [[ 0.99756427  0.          0.06975331  0.4445    ]
    [ 0.          1.          0.          0.        ]
    [-0.06975331  0.          0.99756427  0.09525   ]
    [ 0.          0.          0.          1.        ]]

    Camera relative to Velodyne
    [[ 0.99980379  0.          0.0198087  -0.05929486]
    [ 0.          1.          0.          0.        ]
    [-0.0198087   0.          0.99980379 -0.08562051]
    [ 0.          0.          0.          1.        ]]

    Overall camera to velodyne transform
    Translation (x, y, z): -0.059294861111785835 0.0 -0.08562051124429254
    Rotation (y, p, r): 0.0 0.019810000000000008 0.0
    """

    print("Camera static transform: ")
    # Add values for the camera to base here
    camera_to_base = static_transform_to_extrinsic([0.5080, 0.0, 0.1778, 0, 0.05, 0])
    print(camera_to_base)

    print("Velodyne static transform: ")
    # Add values for the velodyne to base here
    velodyne_to_base = static_transform_to_extrinsic(
        [0.4445, 0.0, 0.09525, 0.0, 0.06981, 0.0]
    )
    print(velodyne_to_base)

    print("Camera relative to Velodyne")
    # Add values for the camera to velodyne here
    camera_to_velodyne = get_relative_transformation(camera_to_base, velodyne_to_base)
    print(camera_to_velodyne)

    print("Overall camera to velodyne transform")
    x, y, z, yaw, pitch, roll = extrinsic_to_static_transform(camera_to_velodyne)
    print("Translation (x, y, z):", x, y, z)
    print("Rotation (y, p, r):", yaw, pitch, roll)
