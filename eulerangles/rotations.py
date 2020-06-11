import numpy as np

from .conventions import AngleConvention


class Angles(np.ndarray, AngleConvention):
    """
    Convenience for managing arrays of angles in degree/radians
    """

    def __new__(cls, theta: np.ndarray = None, units: str = None, positive_ccw: bool = None):
        obj = np.asarray(theta, dtype=np.float).view(cls)
        obj.__init__(theta, units, positive_ccw)
        return obj

    def __init__(self, theta: np.ndarray = None, units: str = None, positive_ccw: bool = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.units = units
        self.positive_ccw = positive_ccw

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.units = getattr(obj, 'units', None)
        self.positive_ccw = getattr(obj, 'positive_ccw', None)

    def sin(self):
        if self.units == 'degrees':
            return np.sin(np.deg2rad(self))
        elif self.units == 'radians':
            return np.sin(self)
        self._invalid_units()

    def cos(self):
        if self.units == 'degrees':
            return np.cos(np.deg2rad(self))
        elif self.units == 'radians':
            return np.cos(self)
        self._invalid_units()

    def as_degrees(self):
        if self.units == 'degrees':
            return self
        elif self.units == 'radians':
            obj = np.deg2rad(self)
            obj.units = 'radians'
            return obj
        else:
            self._invalid_units()

    def as_radians(self):
        if self.units == 'radians':
            return self
        elif self.units == 'degrees':
            obj = np.rad2deg(self)
            obj.units = 'radians'
            return obj
        else:
            self._invalid_units()

    def _invalid_units(self):
        raise AttributeError(f"Units improperly set as {self.units} instead of 'degrees' or 'radians'")


class RotationMatrix(np.ndarray):
    """
    Rotation matrices as (n, 3, 3) numpy arrays with attributes describing the rotations they parametrise
    """

    def __new__(cls, rotation_matrix_array: np.ndarray = None, theta: Angles = None, axis: str = None, **kwargs):
        """
        Initialisation of rotation matrix object, used by view method of np.ndarray
        :param **kwargs:
        :param **kwargs:
        :param rotation_matrix_array: (3, 3) or (n, 3, 3) rotation matrices
        :param axis: (optional) string containing info about any axes relative to which the rotation is defined
        """
        # Flow control, are we creating
        # 1) array from an array containing rotation matrices
        # 2) rotation matrices from theta and axis (uses Theta2RotationMatrix object)
        # 3) empty instance?
        if rotation_matrix_array is not None:
            obj = np.asarray(rotation_matrix_array, dtype=np.float).view(cls)
        elif (rotation_matrix_array is None
              and
              all([argument is not None for argument in (theta, axis)])
              and
              len(axis) == 1):
            rotation_matrix_array = theta2rotm(theta, axis)
            obj = np.asarray(rotation_matrix_array, dtype=np.float).view(cls)
        elif theta is not None:
            obj = np.zeros((theta.size, 3, 3), dtype=np.float).view(cls)
        return obj

    def __array_finalize_(self, obj):
        if obj is None:
            return
        self._single_matrix_sanitation()
        self.axis = getattr(obj, 'axis', None)

    def _single_matrix_sanitation(self):
        """
        Checks for the case where a single rotation matrix is generated (has shape (1, 3, 3)) and reshapes to (3, 3)
        """
        if self.shape == (1, 3, 3):
            return self.reshape((3, 3))
        return self

#
# def axis_check(axis: str):
#     axis = axis.strip()
#     if len(axis) == 1 and axis in ('x', 'y', 'z'):
#         return True
#     return False
