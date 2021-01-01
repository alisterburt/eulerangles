import numpy as np

from .eulers_to_rotation_matrix import euler2matrix
from .rotation_matrix_to_eulers import matrix2euler
from .rotation_matrices.utils import invert_rotation_matrices


def euler2euler(euler_angles: np.ndarray,
                source_axes: str,
                source_right_handed_rotation: bool,
                source_intrinsic: bool,
                target_axes: str,
                target_right_handed_rotation: bool,
                target_intrinsic: bool,
                invert_matrix: bool):
    """
    Convert a set of Euler angles defined one way into a set of Euler angles defined another way.

    Parameters
    ----------
    euler_angles : (n, 3) or (3,) array
        Euler angles to convert
    source_axes : str
        valid sequence of three non-sequential axes from 'x', 'y' and 'z'
    source_right_handed_rotation : bool
        True - Euler angles are interpreted as right handed rotations
        False - Euler angles are interpreted as left handed rotations
    source_intrinsic : bool
        True - Euler angles are interpreted as intrinsic rotations
        False - Euler angles are interpreted as extrinsic rotations
    target_axes : str
        valid sequence of three non-sequential axes from 'x', 'y' and 'z'
    target_right_handed_rotation : bool
        True - Euler angles are interpreted as right handed rotations
        False - Euler angles are interpreted as left handed rotations
    target_intrinsic : bool
        True - Euler angles are interpreted as intrinsic rotations
        False - Euler angles are interpreted as extrinsic rotations
    invert_matrix : bool
        True - rotation matrices will be inverted prior to deriving new Euler angles
        False - rotation matrices will not be inverted prior to deriving new Euler angles

    Returns
    -------
    euler_angles : (n, 3) or (3,) array
        Euler angles generated from input Euler angles
    """
    # Calculate rotation matrices from euler angles
    rotation_matrices = euler2matrix(euler_angles,
                                     source_axes,
                                     source_intrinsic,
                                     source_right_handed_rotation)

    # Invert matrices if one set of euler angles describe the inverse rotations of the desired
    # result
    if invert_matrix:
        rotation_matrices = invert_rotation_matrices(rotation_matrices)

    # Calculate euler angles in the target convention
    euler_angles = matrix2euler(rotation_matrices,
                                target_axes,
                                target_intrinsic,
                                target_right_handed_rotation)
    return euler_angles.squeeze()


