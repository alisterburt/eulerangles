import numpy as np
from typing import Sequence


def compose_matrices_instrinsic(elemental_rotations: Sequence[np.ndarray]):
    """
    Compose three sets of elemental rotation matrices intrinsically.

    Intrinsic rotations correspond to sequential rotations of a coordinate system which is
    mobile, moving with the rigid body after each rotation.

    axes = ax1, ax2, ax3
    angles = a, b, c
    R =  R1(a) * R2(b) * R3(c)

    Parameters
    ----------
    elemental_rotations : sequence of three (n, 3, 3) arrays
                          arrays contain elemental rotation matrices to be composed

    Returns
    -------
    rotation_matrices : (n, 3, 3) array
                        result of intrinsic composition of the elemental matrices

    """

    rotation_matrices = elemental_rotations[0] @ elemental_rotations[1] @ elemental_rotations[2]
    return rotation_matrices


def compose_matrices_extrinsic(elemental_rotations: Sequence[np.ndarray]):
    """
    Compose three sets of elemental rotation matrices extrinsically.

    Intrinsic rotations correspond to sequential rotations within a coordinate system which is
    fixed relative to a rotating rigid body.

    Extrinsic case,
    axes = ax1, ax2, ax3
    angles = a, b, c
    R =  R3(c) * R2(b) * R1(a)

    Parameters
    ----------
    elemental_rotations : sequence of three (n, 3, 3) arrays
                          arrays contain elemental rotation matrices to be composed

    Returns
    -------
    rotation_matrices : (n, 3, 3) array
                        result of intrinsic composition of the elemental matrices


    """
    rotation_matrices = elemental_rotations[2] @ elemental_rotations[1] @ elemental_rotations[0]
    return rotation_matrices


def compose_rotation_matrices(elemental_rotations: Sequence[np.ndarray], mode: str):
    """
    Compose three sets of elemental rotation matrices either intrinsically or extrinsically

    Parameters
    ----------
    elemental_rotations : sequence of three (n, 3, 3) arrays
                          arrays contain elemental rotation matrices to be composed
    mode : str
           either 'intrinsic' or 'extrinsic' depending upon desired mode of composition

    Returns
    -------
    rotation_matrices : (n, 3, 3) array
                        result of intrinsic composition of the elemental matrices
    """
    if mode == 'intrinsic':
        rotation_matrices = compose_matrices_instrinsic(elemental_rotations)
    elif mode == 'extrinsic':
        rotation_matrices = compose_matrices_extrinsic(elemental_rotations)
    else:
        raise ValueError("mode must be 'intrinsic' or 'extrinsic'")
    return rotation_matrices
