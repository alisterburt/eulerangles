import numpy as np


class MatrixFromTheta:
    """
    Object for generating matrices for elemental rotations around the x-, y- or z-axis for a set of angles in degrees
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
        self._single_matrix_check()

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

    def _single_matrix_check(self):
        """
        Decorator which checks for the case where a single rotation matrix is generated (has shape (1, 3, 3)) and
        reshapes to (3, 3) for ease
        """
        if self.rotation_matrices.shape[0] == 1:
            self.rotation_matrices = self.rotation_matrices.reshape((3, 3))

    def get_rotation_matrix(self):
        return self.rotation_matrices

    def get_rotation_matrices(self):
        return self.rotation_matrices


def generate_elemental_rotation_matrix(theta: np.ndarray, axis: str):
    """
    Calculates a set of rotation matrices for CCW rotations around either the 'x', 'y' or 'z' axes by an angle
    (or angles) of theta
    :param theta: number or array-like object of rotation angles in degrees
    :param axis: 'x', 'y' or 'z' axis about which rotation will occur
    :return: rotation matrix or rotation matrices
    """
    angle_calculator = MatrixFromTheta(theta, axis)
    rotation_matrices = angle_calculator.get_rotation_matrices()
    return rotation_matrices
