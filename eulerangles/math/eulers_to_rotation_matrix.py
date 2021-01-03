import numpy as np

from .rotation_matrices.angle_to_matrix import theta2rotm
from .rotation_matrices.rotation_matrix_composition import compose_rotation_matrices
from .constants import valid_axes


def euler2matrix(euler_angles: np.ndarray,
                 axes: str,
                 intrinsic: bool,
                 right_handed_rotation: bool) -> np.ndarray:
    """
    Derive rotation matrices from a set of euler angles.

    Parameters
    ----------
    euler_angles : (n, 3) or (3,) array
        euler angles (in degrees)
    axes : str
        valid sequence of three non-sequential axes from 'x', 'y' and 'z'
        e.g. 'zyz', 'zxz', 'xyz'
    intrinsic : bool
        True - Euler angles are interpreted as intrinsic rotations
        False - Euler angles are interpreted as extrinsic rotations
    right_handed_rotation : bool
        True - Euler angles are interpreted as right handed rotations
        False - Euler angles are interpreted as left handed rotations

    Returns
    -------
    rotation_matrices : (n, 3, 3) or (3, 3) array
        rotation matrices derived from euler angles.

    """
    # Check and santise input
    euler_angles = np.asarray(euler_angles).reshape((-1, 3))
    axes_sanitised = axes.strip().lower()

    if axes_sanitised not in valid_axes:
        raise ValueError(f'Axes {axes} are not a valid set of euler angle axes')

    axes = axes_sanitised

    # Calculate elemental rotation matrices from euler angles
    if not right_handed_rotation:
        # Left handed rotation case
        euler_angles = euler_angles * -1

    elemental_rotations = [theta2rotm(theta=euler_angles[:, idx], axis=axes[idx])
                           for idx in range(3)]

    # Compose final rotation matrices from elemental rotation matrices
    if intrinsic:
        mode = 'intrinsic'
    else:
        mode = 'extrinsic'

    rotation_matrices = compose_rotation_matrices(elemental_rotations, mode=mode)

    return rotation_matrices.squeeze()
