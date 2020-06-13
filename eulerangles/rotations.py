import numpy as np

from .conversions import theta2rotm


class RotX(np.ndarray):
    """
    Rotation matrix or matrices for rotation around the x-axis by theta
    positive is ccw when looking at the origin against the axis
    """

    def __new__(cls, theta: np.ndarray):
        obj = theta2rotm(theta, axis='x')


class RotY(np.ndarray):
    """
    Rotation matrix or matrices for rotation around the y-axis by theta
    positive is ccw when looking at the origin against the axis
    """

    def __new__(cls, theta: np.ndarray):
        obj = theta2rotm(theta, axis='y')


class RotZ(np.ndarray):
    """
    Rotation matrix or matrices for rotation around the y-axis by theta
    positive is ccw when looking at the origin against the axis
    """

    def __new__(cls, theta: np.ndarray):
        obj = theta2rotm(theta, axis='z')
