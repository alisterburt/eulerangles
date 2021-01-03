import numpy as np

from .constants import valid_axes


def matrix2xyx_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rx(k3) @ Ry(k2) @ Rx(k1) = [[c2, s1s2, c1s2],
                                [s2s3, -s1c2s3+c1c3, -c1c2s3-s1c3],
                                [-s2c3, s1c2c3+c1s3, c1c2c3-s1s3]]
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
    angles_radians[idx, 2] = np.arctan2(r32, -r12)

    # convert to degrees
    euler_angles = np.rad2deg(angles_radians)
    return euler_angles


def matrix2zxz_extrinsic(rotation_matrices: np.ndarray) -> np.ndarray:
    """
    Rz(k3) @ Rx(k2) @ Rz(k1) = [[-s1c2s3+c1c3, -c1c2s3-s1c3, s2s3],
                                [s1c2c3+s1s3, c1c2c3-s1s3, -s2c3],
                                [s1s2, c1s2, c2]]
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
    r21 = rotation_matrices[idx, 1, 0]
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
    r33 = rotation_matrices[idx, 2, 2]
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
    matrix2euler_function = extrinsic_matrix2euler_functions[axes]
    return matrix2euler_function(rotation_matrices)


def matrix2euler_intrinsic(rotation_matrices: np.ndarray, axes: str):
    """
    It can be shown that a set of intrinsic rotations about axes x then y then z through angles
    α, β, γ is equivalent to a set of extrinsic rotations about axes z then y then x
    by angles γ, β, α.
    """
    extrinsic_axes = axes[::-1]
    extrinsic_eulers = matrix2euler_extrinsic(rotation_matrices, extrinsic_axes)
    intrinsic_eulers = extrinsic_eulers[:, ::-1]
    return intrinsic_eulers


def matrix2euler_right_handed(rotation_matrices: np.ndarray, axes: str, intrinsic: bool):
    if intrinsic:
        return matrix2euler_intrinsic(rotation_matrices, axes)
    else:
        return matrix2euler_extrinsic(rotation_matrices, axes)


def matrix2euler(rotation_matrices: np.ndarray,
                 axes: str,
                 intrinsic: bool,
                 right_handed_rotation: bool,
                 ) -> np.ndarray:
    """
    Derive a set of euler angles from a set of rotation matrices.

    Parameters
    ----------
    rotation_matrices : (n, 3, 3) or (3, 3) array of float
        rotation matrices from which euler angles are derived
    axes : str
        valid sequence of three non-sequential axes from 'x', 'y' and 'z'
        e.g. 'zyz', 'zxz', 'xyz'
    intrinsic : bool
        True - Euler angles are for intrinsic rotations
        False - Euler angles are for extrinsic rotations
    right_handed_rotation : bool
        True - Euler angles are for right handed rotations
        False - Euler angles are for left handed rotations

    Returns
    -------
    euler_angles : (n, 3) or (3,) array
        Euler angles derived from rotation matrices
    """
    # Sanitise and check input
    rotation_matrices = np.asarray(rotation_matrices).reshape((-1, 3, 3))
    formatted_axes = axes.strip().lower()

    if formatted_axes not in valid_axes:
        raise ValueError(f'Axes {axes} are not a valid set of euler angle axes')

    axes = formatted_axes

    # Calculate euler angles for right handed rotations
    euler_angles = matrix2euler_right_handed(rotation_matrices, axes, intrinsic)

    # If you want left handed rotations, invert the angles
    if not right_handed_rotation:
        euler_angles *= -1

    return euler_angles.squeeze()


extrinsic_matrix2euler_functions = {
    'xyz': matrix2xyz_extrinsic,
    'xyx': matrix2xyx_extrinsic,
    'xzx': matrix2xzx_extrinsic,
    'xzy': matrix2xzy_extrinsic,
    'yxy': matrix2yxy_extrinsic,
    'yxz': matrix2yxz_extrinsic,
    'yzx': matrix2yzx_extrinsic,
    'yzy': matrix2yzy_extrinsic,
    'zxy': matrix2zxy_extrinsic,
    'zxz': matrix2zxz_extrinsic,
    'zyx': matrix2zyx_extrinsic,
    'zyz': matrix2zyz_extrinsic,
}
