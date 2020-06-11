import numpy as np

from .conventions import euler_angle_conventions, EulerAngleConvention


class EulerAngles(np.ndarray, EulerAngleConvention):
    """
    Management of euler angles
    """

    def __new__(cls, euler_angles: np.ndarray, convention: str = None, axes: str = None, intrinsic: bool = None,
                extrinsic: bool = None, positive_ccw: str = None, *args, **kwargs):
        obj = np.asarray(euler_angles).view(cls)
        obj.convention = convention
        obj.check_shape()
        obj.__init__(axes=axes, intrinsic=intrinsic, extrinsic=extrinsic, positive_ccw=positive_ccw, *args, **kwargs)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.convention = getattr(obj, 'convention', None)
        self.check_shape()

    def __init__(self, euler_angles: np.ndarray = None, convention: str = None, axes: str = None,
                 intrinsic: bool = None,
                 extrinsic: bool = None, positive_ccw: str = None, *args, **kwargs):
        EulerAngleConvention.__init__(axes=axes)

    @property
    def convention(self):
        return self._convention

    @convention.setter
    def convention(self, convention: str):
        if convention is None:
            self._convention = None
            return

        if isinstance(convention, str):
            convention = convention.strip().lower()
            try:
                convention = euler_angle_conventions[convention]
                self._convention = convention
                return
            except NotImplementedError:
                error_message = f"Euler angle convention for '{convention} is unavailable'"
                raise NotImplementedError(error_message)

        elif not isinstance(convention, EulerAngleConvention):
            error_message = """convention should be a string corresponding to the name of the software package in which 
            the euler angles were defined or an EulerAngleConvention object"""
            raise ValueError(error_message)


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


def rotm2xyx
