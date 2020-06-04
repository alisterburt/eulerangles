import numpy as np


class RotationMatrix(np.ndarray):
    """
    Rotation matrices as (n, 3, 3) numpy arrays with attributes describing the rotations they parametrise
    """

    def __new__(cls, rotation_matrix_array: np.ndarray = None, theta: np.ndarray = None, axis: str = None,
                positive_ccw: bool = None, **kwargs):
        """
        Initialisation of rotation matrix object, used by view method of np.ndarray
        :param **kwargs:
        :param rotation_matrix_array: (3, 3) or (n, 3, 3) rotation matrices
        :param theta: (optional) angles from which RotationMatrix can be derived
        :param axis: (optional) string containing info about any axes relative to which the rotation is defined
        :param positive_ccw: (optional) boolean describing whether the rotation
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

        # Add attributes
        obj.theta = obj.set_theta(theta)
        obj.axis = obj.set_axis(axis)
        obj.positive_ccw = positive_ccw

        # Reshape if single matrix only
        obj = obj.single_matrix_sanitation()
        return obj

    def __array_finalize_(self, obj):
        if obj is None:
            return
        self.axis = getattr(obj, 'axis', None)
        self.positive_ccw = getattr(obj, 'positive_ccw', None)

    def set_axis(self, axis):
        if axis is None:
            self.axes = axis
            return

        elif all([axis.lower() in ('x', 'y', 'z') for axis in axis]):
            self.axes = axis.lower()
            return

        elif isinstance(axis, np.ndarray) and axis.size == 3:
            error_message = 'Quaternions are not yet implemented'
            raise NotImplementedError(error_message)

        error_message = "Axis must be 'x', 'y' or 'z' or a combination thereof such as 'zxz'"
        raise ValueError(error_message)

    def set_theta(self, theta: np.ndarray):
        self.theta = np.asarray(theta)

    def single_matrix_sanitation(self):
        """
        Checks for the case where a single rotation matrix is generated (has shape (1, 3, 3)) and reshapes to (3, 3)
        """
        if self.shape == (1, 3, 3):
            return self.reshape((3, 3))
        return self


class Theta2RotationMatrix:
    """
    Object for generating matrices for elemental rotations around the x-, y- or z-axis for a set of angles in degrees
    Positive values of theta rotate a point ccw around an axis when looking from a positive position on that axis
    towards the origin
    """

    def __init__(self, theta: np.ndarray, axis: str, calculate=True):
        self._preprocess(theta, axis)
        if calculate:
            self.generate_rotation_matrices()

    def _preprocess(self, theta: np.ndarray, axis: str):
        self._prepare_theta(theta)
        self._prepare_sin_theta()
        self._prepare_cos_theta()
        self.n = self.theta.size
        self.set_axis(axis)
        self._prepare_empty_rotation_matrix()

    def generate_rotation_matrices(self):
        if self.axis == 'x':
            self.generate_rotation_matrices_x()
        elif self.axis == 'y':
            self.generate_rotation_matrices_y()
        elif self.axis == 'z':
            self.generate_rotation_matrices_z()
        self.rotation_matrices = RotationMatrix(self.rotation_matrices,
                                                theta=self.theta,
                                                axis=self.axis,
                                                positive_ccw=True)

    def _prepare_theta(self, theta: np.ndarray):
        """
        Prepare theta input in degrees for rotation function vectorisation
        :param theta: array-like object containing theta in radians
        """
        self.theta = np.asarray(np.deg2rad(theta)).reshape(-1)

    def _prepare_sin_theta(self):
        self.sin_theta = np.sin(self.theta)

    def _prepare_cos_theta(self):
        self.cos_theta = np.cos(self.theta)

    def _prepare_empty_rotation_matrix(self):
        """
        Prepare an empty (n, 3, 3) array for vectorised rotation matrix generation
        """
        shape = (self.n, 3, 3)
        self.rotation_matrices = np.zeros(shape, dtype=np.float)

    def generate_rotation_matrices_x(self):
        """
        vectorised calculation the rotation matrix for an anticlockwise rotation around the x-axis
        by the angle theta

        rotation_matrix = np.array([[1, 0, 0],
                                    [0, cos_theta, -sin_theta],
                                    [0, sin_theta, cos_theta]],
                                   dtype=np.float)

        :return: rotation_matrix (3,3) or rotation_matrices (n,3,3)
        """
        # Generate rotation matrices
        self.rotation_matrices[:, 0, 0] = 1
        self.rotation_matrices[:, (1, 2), (2, 1)] = self.cos_theta.reshape((self.n, 1))
        self.rotation_matrices[:, 2, 1] = self.sin_theta
        self.rotation_matrices[:, 1, 2] = -self.sin_theta

    def generate_rotation_matrices_y(self):
        """
        calculates the rotation matrix for a passive anticlockwise rotation around the y-axis
        by the angle theta

        rotation_matrix = np.array([[cos_theta, 0, sin_theta],
                                    [0, 1, 0],
                                    [-sin_theta, 0, cos_theta]],
                                   dtype=np.float)
        """
        # Generate rotation matrices
        self.rotation_matrices[:, (0, 2), (0, 2)] = self.cos_theta.reshape(self.n, 1)
        self.rotation_matrices[:, 1, 1] = 1
        self.rotation_matrices[:, 0, 2] = self.sin_theta
        self.rotation_matrices[:, 2, 0] = -self.sin_theta

    def generate_rotation_matrices_z(self):
        """
        calculates the rotation matrix for a passive anticlockwise rotation around the z-axis
        by the angle theta

        rotation_matrix = np.array([[cos_theta, -sin_theta, 0],
                                    [sin_theta, cos_theta, 0],
                                    [0, 0, 1]],
                                   dtype=np.float)
        """
        # Generate rotation matrices
        self.rotation_matrices[:, (0, 1), (0, 1)] = self.cos_theta.reshape(self.n, 1)
        self.rotation_matrices[:, 0, 1] = -self.sin_theta
        self.rotation_matrices[:, 1, 0] = self.sin_theta
        self.rotation_matrices[:, 2, 2] = 1

    def set_axis(self, axis: str):
        """
        Makes sure axis entry is lowercase x, y or z
        :param axis: str 'x', 'y' or 'z'
        :return: axis
        """
        if axis.lower() in ('x', 'y', 'z'):
            self.axis = axis.lower()
            return

        error_message = "Axis must be one of 'x', 'y' or 'z'"
        raise ValueError(error_message)

    def get_rotation_matrix(self):
        return self.rotation_matrices

    def get_rotation_matrices(self):
        return self.rotation_matrices


class RotX(RotationMatrix):
    def __new__(cls, theta: np.ndarray):
        obj = super().__new__(RotationMatrix, theta=theta, axis='x')
        return obj


class RotY(RotationMatrix):
    def __new__(cls, theta: np.ndarray):
        obj = super().__new__(RotationMatrix, theta=theta, axis='y')
        return obj


class RotZ(RotationMatrix):
    def __new__(cls, theta: np.ndarray):
        obj = super().__new__(RotationMatrix, theta=theta, axis='z')
        return obj


def theta2rotm(theta: np.ndarray, axis: str):
    """
    Calculates a set of rotation matrices for CCW rotations around either the 'x', 'y' or 'z' axes by an angle
    (or angles) of theta
    :param theta: number or array-like object of rotation angles in degrees
    :param axis: 'x', 'y' or 'z' axis about which rotation will occur
    :return: rotation matrix or array of rotation matrices
    """
    matrix_calculator = Theta2RotationMatrix(theta, axis)
    rotation_matrices = matrix_calculator.get_rotation_matrices()
    return rotation_matrices
