import numpy as np


def theta2rotx(theta: np.ndarray) -> np.ndarray:
    """
    Rx = [[1, 0, 0],
          [0, c(t), -s(t)],
          [0, s(t), c(t)]]
    :param theta: angle(s) in degrees, positive is counterclockwise
    :return: rotation_matrices
    """
    theta = np.deg2rad(np.asarray(theta).reshape(-1))
    rotation_matrices = np.zeros((theta.shape[0], 3, 3), dtype=float)
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
    rotation_matrices = np.zeros((theta.shape[0], 3, 3), dtype=float)
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
    rotation_matrices = np.zeros((theta.shape[0], 3, 3), dtype=float)
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
