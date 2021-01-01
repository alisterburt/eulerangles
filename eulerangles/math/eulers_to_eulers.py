from typing import Union

import numpy as np

from .eulers_to_rotation_matrix import euler2matrix
from .rotation_matrix_to_eulers import matrix2euler
from .rotation_matrices.utils import invert_rotation_matrices


def euler2euler(euler_angles: np.ndarray,
                source_axes: str,
                source_positive_ccw: bool,
                source_intrinsic: bool,
                target_axes: str,
                target_positive_ccw: bool,
                target_intrinsic: bool,
                invert_matrix: bool):
    # Calculate rotation matrices from euler angles
    rotation_matrices = euler2matrix(euler_angles,
                                     source_axes,
                                     source_intrinsic,
                                     source_positive_ccw)

    # Invert matrices if one set of euler angles describe the inverse rotations of the desired
    # result
    if invert_matrix:
        rotation_matrices = invert_rotation_matrices(rotation_matrices)

    # Calculate euler angles in the target convention
    euler_angles = matrix2euler(rotation_matrices,
                                target_axes,
                                target_intrinsic,
                                target_positive_ccw)
    return euler_angles.squeeze()


