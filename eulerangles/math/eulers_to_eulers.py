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
    return euler_angles



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
        rotation_matrices = invert_rotation_matrices(rotation_matrices)

    # Calculate euler angles in the target convention
    euler_angles = matrix2euler(rotation_matrices, tc.axes, tc.positive_ccw, tc.intrinsic,
                                tc.extrinsic)
    return euler_angles
