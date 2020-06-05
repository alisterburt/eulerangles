import numpy as np

from .conventions import EulerAngleConventions as euler_angle_conventions


class EulerAngleConvention:
    """
    Euler angle conventions used by different softwares in electron microscopy
    """

    def __init__(self,
                 name: str,
                 axes: str,
                 reference_frame: str,
                 positive_ccw: bool,
                 intrinsic: bool):
        self.name = name
        self.axes = axes
        self.reference_frame = reference_frame
        self.positive_ccw = positive_ccw
        self.intrinsic = intrinsic

    def __repr__(self):
        return (
            'Euler Angle Convention\n'
            f'Name: {self.name}\n'
            f'Axes: {self.axes}\n'
            f'Reference Frame: {self.reference_frame}\n'
            f'Positive Angles are CCW rotations looking against the axis? {self.positive_ccw}\n'
            f'Euler angles describe intrinsic rotations? {self.intrinsic}\n'
        )


class EulerAngles(np.ndarray):
    """
    Management of euler angles
    """

    def __new__(cls, euler_angles: np.ndarray, convention: str = None):
        obj = np.asarray(euler_angles).view(cls)
        obj.convention = obj.set_convention(convention)
        obj.check_shape()
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.convention = getattr(obj, 'convention', None)
        self.check_shape()

    def set_convention(self, convention):
        if isinstance(convention, str):
            convention = convention.strip().lower()
            try:
                convention = euler_angle_conventions[convention]
            except:
                error_message = f"Euler angle convention for '{convention} is unavailable'"
                raise NotImplementedError(error_message
                                          )
        elif not isinstance(convention, EulerAngleConvention):
            error_message = """convention should be a string corresponding to the name of the software package in which 
            the euler angles were defined"""
            raise ValueError(error_message)

        return convention

    def check_shape(self):
        if self.shape[1] != 3:
            error_message = 'eulers angles should be an (n, 3) array-like object'
            raise ValueError(error_message)


def euler2matrix(euler_angles: EulerAngles, convention: EulerAngleConvention = None):
    if convention is None:
        assert hasattr(euler_angles, 'convention'), 'euler angles must have a convention if one is not supplied'

    euler_angles = EulerAngle(euler_angles, convention)
    rotation_matrices = euler_angles.to_rotation_matrices()
    return rotation_matrices
