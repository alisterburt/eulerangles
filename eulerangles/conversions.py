from typing import Union
from warnings import warn

import numpy as np

from .conventions import EulerAngleConvention, get_convention


def theta2rotx(theta: np.ndarray) -> np.ndarray:
    """
    Rx = [[1, 0, 0],
          [0, c(t), -s(t)],
          [0, s(t), c(t)]]
    :param theta: angle(s) in degrees, positive is counterclockwise
    :return: rotation_matrices
    """
    theta = np.deg2rad(np.asarray(theta).reshape(-1))
    rotation_matrices = np.zeros((theta.shape[0], 3, 3), dtype=np.float)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    rotation_matrices[:, 0, 0] = 1
    rotation_matrices[:, (1, 2), (1, 2)] = cos_theta[:, np.newaxis]
    rotation_matrices[:, 1, 2] = -sin_theta
    rotation_matrices[:, 2, 1] = sin_theta
    return rotation_matrices


def theta2roty(theta: np.ndarray) -> np.ndarray:
    """
    Ry = [[c(t), 0, s(t)],
          [0, 1, 0],
          [-s(t), 0, c(t)]]
    :param theta: angle(s) in degrees, positive is counterclockwise
    :return: rotation_matrices
    """
    theta = np.deg2rad(np.asarray(theta).reshape(-1))
    rotation_matrices = np.zeros((theta.shape[0], 3, 3), dtype=np.float)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    rotation_matrices[:, 1, 1] = 1
    rotation_matrices[:, (0, 2), (0, 2)] = cos_theta[:, np.newaxis]
    rotation_matrices[:, 0, 2] = sin_theta
    rotation_matrices[:, 2, 0] = -sin_theta
    return rotation_matrices


def theta2rotz(theta: np.ndarray) -> np.ndarray:
    """
    Rz = [[c(t), -s(t), 0],
          [s(t), c(t), 0],
          [0, 0, 1]]
    :param theta: angle(s) in degrees, positive is counterclockwise
    :return: rotation_matrices
    """
    theta = np.deg2rad(np.asarray(theta).reshape(-1))
    rotation_matrices = np.zeros((theta.shape[0], 3, 3), dtype=np.float)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    rotation_matrices[:, 2, 2] = 1
    rotation_matrices[:, (0, 1), (0, 1)] = cos_theta[:, np.newaxis]
    rotation_matrices[:, 0, 1] = -sin_theta
    rotation_matrices[:, 1, 0] = sin_theta
    return rotation_matrices


def theta2rotm(theta: np.ndarray, axis: str):
    """
    Convert values for theta into rotation matrices around a given axis 'x', 'y' or 'z'
    :param theta: angle(s) in degrees, positive is counterclockwise
    :param axis: 'x', 'y' or 'z'
    :return: rotation_matrices
    """
    axis = axis.strip().lower()
    if axis not in ('x', 'y', 'z'):
        raise ValueError(f"Axis must be one of 'x', 'y' or 'z''")
    elif axis == 'x':
        rotation_matrices = theta2rotx(theta)
    elif axis == 'y':
        rotation_matrices = theta2roty(theta)
    elif axis == 'z':
        rotation_matrices = theta2rotz(theta)
    if rotation_matrices.shape[0] == 1:
        rotation_matrices = rotation_matrices.reshape((3, 3))
    return rotation_matrices


def euler2matrix(euler_angles: np.ndarray, axes: str, intrinsic: bool = None, extrinsic: bool = None,
                 positive_ccw: bool = None) -> np.ndarray:
    """

    :param positive_ccw:
    :param euler_angles:
    :param axes:
    :param intrinsic:
    :param extrinsic:
    :return: rotation_matrices (n, 3, 3)
    """
    # Check input
    euler_angles = np.asarray(euler_angles).reshape((-1, 3))
    axes = axes.strip().lower()
    if axes not in ('xyx', 'yzy', 'zxz', 'xzx', 'yxy', 'zyz', 'xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'):
        raise ValueError(f'Axes {axes} are not a valid set of euler angle axes')

    # Calculate elemental rotation matrices from euler angles
    # Make sure your rotation angles have the correct sign
    if positive_ccw is None:
        warn('positive_ccw was not explicitly set, defaulting to considering positive angles as CCW rotations')
        positive_ccw = True
    if positive_ccw:
        # RotationMatrix object creates matrices representing ccw positive rotations looking against axis
        elemental_rotations = [theta2rotm(theta=euler_angles[:, ax_idx], axis=axes[ax_idx]) for ax_idx in range(3)]
    else:
        # While positive ccw looking against axis is standard in maths and physics, some people define positive to
        # mean a clockwise rotation when looking against the axis
        # The effect of this is we need to reverse the sign of the angle to use it with our rotation matrix
        # definitions which are positive ccw looking against the axis.
        elemental_rotations = [theta2rotm(theta=-1 * euler_angles[:, ax_idx], axis=axes[ax_idx]) for ax_idx in range(3)]

    # Compose final rotation matrices from elemental rotation matrices
    if intrinsic and extrinsic:
        raise ValueError(f"Only one of 'intrinsic': {intrinsic} and 'extrinsic': {extrinsic} can be set to True")

    elif intrinsic:
        # Intrinsic case,
        # axes = ax1, ax2, ax3
        # angles = a, b, c
        # R =  R1(a) * R2(b) * R3(c)
        rotation_matrices = elemental_rotations[0] @ elemental_rotations[1] @ elemental_rotations[2]

    elif extrinsic:
        # Extrinsic case,
        # axes = ax1, ax2, ax3
        # angles = a, b, c
        # R =  R3(c) * R2(b) * R1(a)
        rotation_matrices = elemental_rotations[2] @ elemental_rotations[1] @ elemental_rotations[0]
    else:
        raise ValueError(F"One of 'intrinsic': {intrinsic} and 'extrinsic': {extrinsic} must be set to True")

    return rotation_matrices


def matrix2xyx_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rx(k3) @ Ry(k2) @ Rx(k1) = [[c2, s1s2, c1s2],
                                [s2s3, -s1c2s3+c1c3, -c1c2s3-s1c3],
                                [-s2c3, s1c2c3+c1s3, c1c2c3-s1s3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arccos(rotation_matrices[:, 0, 0])

    # Gimbal lock case (s2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 2]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r23 = rotation_matrices[gimbal_idx, 1, 2]
    r22 = rotation_matrices[gimbal_idx, 1, 1]
    angles_radians[gimbal_idx, 0] = np.arctan2(-r23, r22)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r12 = rotation_matrices[idx, 0, 1]
    r13 = rotation_matrices[idx, 0, 2]
    r21 = rotation_matrices[idx, 1, 0]
    r31 = rotation_matrices[idx, 2, 0]
    angles_radians[idx, 0] = np.arctan2(r12, r13)
    angles_radians[idx, 2] = np.arctan2(r21, -r31)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2yzy_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Ry(k3) @ Rz(k2) @ Ry(k1) = [[c1c2c3-s1s3, -s2c3, s1c2c3+c1c3],
                                [c1s2, c2, s1s2],
                                [-c1c2s3, s2s3, -s1c2s3+c1c3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arccos(rotation_matrices[:, 1, 1])

    # Gimbal lock case (s2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 1, 0]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r31 = rotation_matrices[gimbal_idx, 2, 0]
    r33 = rotation_matrices[gimbal_idx, 2, 2]
    angles_radians[gimbal_idx, 0] = np.arctan2(-r31, r33)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r23 = rotation_matrices[idx, 1, 2]
    r21 = rotation_matrices[idx, 1, 0]
    r32 = rotation_matrices[idx, 2, 1]
    r12 = rotation_matrices[idx, 0, 1]
    angles_radians[idx, 0] = np.arctan2(r23, r21)
    angles_radians[idx, 2] = np.arctan2(r32, r12)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)
    return euler_angles


def matrix2zxz_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rz(k3) @ Rx(k2) @ Rz(k1) = [[-s1c2s3+c1c3, -c1c2s3-s1c3, s2s3],
                                [s1c2c3+s1s3, c1c2c3-s1s3, -s2c3],
                                [s1s2, c1s2, c2]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles[:, 1] = np.arccos(rotation_matrices[:, 2, 2])

    # Gimbal lock case (s2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 2]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r12 = rotation_matrices[gimbal_idx, 0, 1]
    r11 = rotation_matrices[gimbal_idx, 0, 0]
    angles[gimbal_idx, 0] = np.arctan2(-r12, r11)
    angles[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r31 = rotation_matrices[idx, 2, 0]
    r32 = rotation_matrices[idx, 2, 1]
    r13 = rotation_matrices[idx, 0, 2]
    r23 = rotation_matrices[idx, 1, 2]
    angles[idx, 0] = np.arctan2(r31, r32)
    angles[idx, 2] = np.arctan2(r13, -r23)

    # convert to degrees
    euler_angles = np.rad2deg(angles)

    return euler_angles


def matrix2xzx_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rx(k3) @ Rz(k2) @ Rx(k1) = [[c2, -c1s2, s1s2],
                                [s2c3, c1c2c3-s3, -s1c2c3-c1s3],
                                [s2s3, c1c2s3+s1c3, -s1c2s3+c1c3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arccos(rotation_matrices[:, 0, 0])

    # Gimbal lock case (s2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 2]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r32 = rotation_matrices[gimbal_idx, 2, 1]
    r33 = rotation_matrices[gimbal_idx, 2, 2]
    angles_radians[gimbal_idx, 0] = np.arctan2(r32, r33)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r13 = rotation_matrices[idx, 0, 2]
    r12 = rotation_matrices[idx, 0, 1]
    r31 = rotation_matrices[idx, 2, 0]
    r21 = rotation_matrices[idx, 1, 0]
    angles_radians[idx, 0] = np.arctan2(r13, -r12)
    angles_radians[idx, 2] = np.arctan2(r31, r21)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)
    return euler_angles


def matrix2yxy_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Ry(k3) @ Rx(k2) @ Ry(k1) = [[-s1c2s3+c1c3, s2s3, c1c2s3+s1c3],
                                [s1s2, c2, -c1s2],
                                [-s1c2c3-c1s3, s2c3, c1c2c3-s1s3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arccos(rotation_matrices[:, 1, 1])

    # Gimbal lock case (s2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 1]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r13 = rotation_matrices[gimbal_idx, 0, 2]
    r11 = rotation_matrices[gimbal_idx, 0, 0]
    angles_radians[gimbal_idx, 0] = np.arctan2(r13, r11)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r21 = rotation_matrices[idx, 1, 0]
    r23 = rotation_matrices[idx, 1, 2]
    r12 = rotation_matrices[idx, 0, 1]
    r32 = rotation_matrices[idx, 2, 1]
    angles_radians[idx, 0] = np.arctan2(r21, -r23)
    angles_radians[idx, 2] = np.arctan2(r12, r32)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2zyz_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rz(k3) @ Ry(k2) @ Rz(k1) = [[c1c2c3-s1s3, -s1c2c3-c1s3, s2c3],
                                [c1c2s3+s1c3, -s1c2s3+c1c3, s2s3],
                                [-c1s2, s1s2, c2]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arccos(rotation_matrices[:, 2, 2])

    # Gimbal lock case (s2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 2]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r21 = rotation_matrices[gimbal_idx, 1, 0]
    r22 = rotation_matrices[gimbal_idx, 1, 1]
    angles_radians[gimbal_idx, 0] = np.arctan2(r21, r22)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r32 = rotation_matrices[idx, 2, 1]
    r31 = rotation_matrices[idx, 2, 0]
    r23 = rotation_matrices[idx, 1, 2]
    r13 = rotation_matrices[idx, 0, 2]
    angles_radians[idx, 0] = np.arctan2(r32, -r31)
    angles_radians[idx, 2] = np.arctan2(r23, r13)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2xyz_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rz(k3) @ Ry(k2) @ Rx(k1) = [[c2c3, s1s2c3-c1s3, c1s2c3+s1s3],
                                [c2s3, s1s2s3+c1c3, c1s2s3-s1c3],
                                [-s2, s1c2, c1c2]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = -np.arcsin(rotation_matrices[:, 2, 0])

    # Gimbal lock case (c2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 0]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r23 = rotation_matrices[gimbal_idx, 1, 2]
    r22 = rotation_matrices[gimbal_idx, 1, 1]
    angles_radians[gimbal_idx, 0] = np.arctan2(-r23, r22)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r32 = rotation_matrices[idx, 2, 1]
    r33 = rotation_matrices[idx, 2, 2]
    r21 = rotation_matrices[idx, 2, 0]
    r11 = rotation_matrices[idx, 0, 0]
    angles_radians[idx, 0] = np.arctan2(r32, r33)
    angles_radians[idx, 2] = np.arctan2(r21, r11)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2yzx_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rx(k3) @ Rz(k2) @ Ry(k1) = [[c1c2, -s2, s1c2],
                                [c1s2c3+s1s3, c2c3, s1s2c3-c1s3],
                                [c1s2s3-s1c3, c2s3, s1s2s3+c1c3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = -np.arcsin(rotation_matrices[:, 0, 1])

    # Gimbal lock case (c2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 0]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r31 = rotation_matrices[gimbal_idx, 2, 0]
    r33 = rotation_matrices[gimbal_idx, 2, 2]
    angles_radians[gimbal_idx, 0] = np.arctan2(-r31, r33)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r13 = rotation_matrices[idx, 0, 2]
    r11 = rotation_matrices[idx, 0, 0]
    r32 = rotation_matrices[idx, 2, 1]
    r22 = rotation_matrices[idx, 1, 1]
    angles_radians[idx, 0] = np.arctan2(r13, r11)
    angles_radians[idx, 2] = np.arctan2(r32, r22)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2zxy_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Ry(k3) @ Rx(k2) @ Rz(k1) = [[s1s2s3+c1c3, c1s2s3-s1c3, c2s3],
                                [s1c2, c1c2, -s2],
                                [s1s2c3-c1s3, c1s2c3+s1s3, c2c3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = -np.arcsin(rotation_matrices[:, 1, 2])

    # Gimbal lock case (c2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 1, 0]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r12 = rotation_matrices[gimbal_idx, 0, 1]
    r11 = rotation_matrices[gimbal_idx, 0, 0]
    angles_radians[gimbal_idx, 0] = np.arctan2(-r12, r11)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r21 = rotation_matrices[idx, 1, 0]
    r22 = rotation_matrices[idx, 1, 1]
    r13 = rotation_matrices[idx, 0, 2]
    r33 = rotation_matrices[idx, 2, 0]
    angles_radians[idx, 0] = np.arctan2(r21, r22)
    angles_radians[idx, 2] = np.arctan2(r13, r33)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2xzy_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Ry(k3) @ Rz(k2) @ Rx(k1) = [[c2c3, -c1s2c3+s1s3, s1s2c3+c1s3],
                                [s2, c1c2, -s1c2],
                                [-c2s3, c1s2s3+s1c3, -s1s2s3+c1c3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arcsin(rotation_matrices[:, 1, 0])

    # Gimbal lock case (c2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 0, 0]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r32 = rotation_matrices[gimbal_idx, 2, 1]
    r33 = rotation_matrices[gimbal_idx, 2, 2]
    angles_radians[gimbal_idx, 0] = np.arctan2(r32, r33)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r23 = rotation_matrices[idx, 1, 2]
    r22 = rotation_matrices[idx, 1, 1]
    r31 = rotation_matrices[idx, 2, 0]
    r11 = rotation_matrices[idx, 0, 0]
    angles_radians[idx, 0] = np.arctan2(-r23, r22)
    angles_radians[idx, 2] = np.arctan2(-r31, r11)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2yxz_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rz(k3) @ Rx(k2) @ Ry(k1) = [[-s1s2s3+c1c3, -c2s3, c1s2s3+s1c3],
                                [s1s2c3+c1s3, c2c3, -c1s2c3+s1s3],
                                [-s1c2, s2, c1c2]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arcsin(rotation_matrices[:, 2, 1])

    # Gimbal lock case (c2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 1, 1]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r13 = rotation_matrices[gimbal_idx, 0, 2]
    r11 = rotation_matrices[gimbal_idx, 0, 0]
    angles_radians[gimbal_idx, 0] = np.arctan2(r13, r11)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r31 = rotation_matrices[idx, 2, 0]
    r33 = rotation_matrices[idx, 2, 2]
    r12 = rotation_matrices[idx, 0, 1]
    r22 = rotation_matrices[idx, 1, 1]
    angles_radians[idx, 0] = np.arctan2(-r31, r33)
    angles_radians[idx, 2] = np.arctan2(-r12, r22)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2zyx_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rx(k3) @ Ry(k2) @ Rz(k1) = [[c1c2, -s1c2, s2],
                                [c1s2s3+s1c3, -s1s2s3+c1c3, -c2s3],
                                [-c1s2c3+s1s3, s1s2c3+c1s3, c2c3]]
    :param rotation_matrices:
    :return: euler_angles
    """
    rotation_matrices = rotation_matrices.reshape((-1, 3, 3))
    angles_radians = np.zeros((rotation_matrices.shape[0], 3))

    # Angle 2 can be taken directly from matrices
    angles_radians[:, 1] = np.arcsin(rotation_matrices[:, 0, 2])

    # Gimbal lock case (c2 = 0)
    tolerance = 1e-4

    # Find indices where this is the case
    gimbal_idx = np.abs(rotation_matrices[:, 1, 1]) < tolerance

    # Calculate angle 1 and set angle 3 = 0 for those indices
    r21 = rotation_matrices[gimbal_idx, 1, 0]
    r22 = rotation_matrices[gimbal_idx, 1, 1]
    angles_radians[gimbal_idx, 0] = np.arctan2(r21, r22)
    angles_radians[gimbal_idx, 2] = 0

    # Normal case (s2 > 0)
    idx = np.invert(gimbal_idx)
    r12 = rotation_matrices[idx, 0, 1]
    r11 = rotation_matrices[idx, 0, 0]
    r23 = rotation_matrices[idx, 1, 2]
    r33 = rotation_matrices[idx, 2, 2]
    angles_radians[idx, 0] = np.arctan2(-r12, r11)
    angles_radians[idx, 2] = np.arctan2(-r23, r33)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)

    return euler_angles


def matrix2euler_extrinsic(rotation_matrices: np.ndarray, axes: str):
    axes = axes.strip().lower()
    if axes not in ('xyx', 'yzy', 'zxz', 'xzx', 'yxy', 'zyz', 'xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'):
        raise ValueError(f'Axes {axes} are not a valid set of euler angle axes')
    elif axes == 'xyx':
        return matrix2xyx_extrinsic(rotation_matrices)
    elif axes == 'yzy':
        return matrix2yzy_extrinsic(rotation_matrices)
    elif axes == 'zxz':
        return matrix2zxz_extrinsic(rotation_matrices)
    elif axes == 'xzx':
        return matrix2xzx_extrinsic(rotation_matrices)
    elif axes == 'yxy':
        return matrix2yzy_extrinsic(rotation_matrices)
    elif axes == 'zyz':
        return matrix2zyz_extrinsic(rotation_matrices)
    elif axes == 'xyz':
        return matrix2xyz_extrinsic(rotation_matrices)
    elif axes == 'yzx':
        return matrix2yzx_extrinsic(rotation_matrices)
    elif axes == 'zxy':
        return matrix2zxy_extrinsic(rotation_matrices)
    elif axes == 'xzy':
        return matrix2xzy_extrinsic(rotation_matrices)
    elif axes == 'yxz':
        return matrix2xzy_extrinsic(rotation_matrices)
    elif axes == 'zyx':
        return matrix2yxz_extrinsic(rotation_matrices)
    raise ValueError('A problem occurred')


def matrix2euler_intrinsic(rotation_matrices: np.ndarray, axes: str):
    """
    It can be shown that a set of intrinsic rotations about axes x then y then z through angles α, β, γ is equivalent
    to a set of extrinsic rotations about axes z then y then x by angles γ, β, α. :param rotation_matrices: :param
    axes: :return:
    """
    extrinsic_axes = axes[::-1]
    extrinsic_eulers = matrix2euler_extrinsic(rotation_matrices, extrinsic_axes)
    intrinsic_eulers = extrinsic_eulers[:, ::-1]
    return intrinsic_eulers


def matrix2euler_positive_ccw(rotation_matrices: np.ndarray, axes: str, intrinsic: bool = None, extrinsic: bool = None):
    """
    Calculates intrinsic or extrinsic euler angles (positive angles are ccw rotations) around a set of three axes from
    a set of rotation matrices
    :param rotation_matrices: rotation matrix (n,3,3) numpy array
    :param axes: 'zxz', 'zyz' or similar, three nonconsecutive axes
    :param intrinsic: fixed object, mobile coordinate system
    :param extrinsic: fixed coordinate system, mobile object
    :return:
    """
    if intrinsic and extrinsic:
        raise ValueError(f"Only one of 'intrinsic' and 'extrinsic' can be True")
    elif intrinsic:
        return matrix2euler_intrinsic(rotation_matrices, axes)
    elif extrinsic:
        return matrix2euler_extrinsic(rotation_matrices, axes)
    raise ValueError(f"Problem, could not interpret intrinsic or extrinsic as True or False")


def matrix2euler(rotation_matrices: np.ndarray, target_axes: str, target_positive_ccw: bool,
                 target_intrinsic: bool = None, target_extrinsic: bool = None) -> np.ndarray:
    if target_positive_ccw:
        euler_angles = matrix2euler_positive_ccw(rotation_matrices, target_axes, target_intrinsic, target_extrinsic)
    elif target_positive_ccw is False:
        euler_angles = matrix2euler_positive_ccw(rotation_matrices, target_axes, target_intrinsic,
                                                 target_extrinsic) * -1

    try:
        if euler_angles.shape[0] == 1:
            euler_angles = euler_angles.reshape(-1)
        return euler_angles

    except NameError:
        raise ValueError(f"Problem, could not interpret positive_ccw as True or False")


def euler2euler(euler_angles: np.ndarray, source_convention: Union[str, EulerAngleConvention],
                target_convention: Union[str, EulerAngleConvention]):
    # Parse conventions
    if isinstance(target_convention, str):
        target_convention = get_convention(target_convention)
    tc = target_convention
    if isinstance(source_convention, str):
        source_convention = get_convention(source_convention)
    sc = source_convention

    # Calculate rotation matrices from euler angles
    rotation_matrices = euler2matrix(euler_angles, sc.axes, sc.intrinsic,
                                     sc.extrinsic, sc.positive_ccw)

    # Invert matrices if one set of eulers describe rotation of the reference and the other
    # rotation of the particles
    # For rotation matrices, inversion is equivalent to the transpose
    if getattr(sc, 'reference_frame', None) != getattr(tc, 'reference_frame', None):
        rotation_matrices = rotation_matrices.transpose((0, 2, 1))

    # Calculate euler angles in the target convention
    euler_angles = matrix2euler(rotation_matrices, tc.axes, tc.positive_ccw, tc.intrinsic, tc.extrinsic)
    return euler_angles
