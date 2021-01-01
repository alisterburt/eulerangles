import numpy as np

from .rotation_matrices.angle_to_matrix import theta2rotm
from .rotation_matrices.rotation_matrix_composition import compose_rotation_matrices
from ..constants import valid_axes


def euler2matrix(euler_angles: np.ndarray,
                 axes: str,
                 intrinsic: bool,
                 positive_ccw: bool) -> np.ndarray:
    """

    :param positive_ccw:
    :param euler_angles:
    :param axes:
    :param intrinsic:
    :return: rotation_matrices (n, 3, 3) or (3, 3)
    """
    # Check and santise input
    euler_angles = np.asarray(euler_angles).reshape((-1, 3))
    axes_sanitised = axes.strip().lower()

    if axes_sanitised not in valid_axes:
        raise ValueError(f'Axes {axes} are not a valid set of euler angle axes')

    axes = axes_sanitised

    # Calculate elemental rotation matrices from euler angles
    # Make sure your rotation angles have the correct sign
    if not positive_ccw:
        # While positive ccw looking against axis is standard in maths and physics,
        # some people define positive to mean a clockwise rotation when looking
        # against the axis.
        # The effect of this is we need to reverse the sign of the angle to use it
        # with our rotation matrix definitions which are positive ccw looking
        # against the axis.
        euler_angles = euler_angles * -1

    elemental_rotations = [theta2rotm(theta=euler_angles[:, idx], axis=axes[idx])
                           for idx in range(3)]

    # Compose final rotation matrices from elemental rotation matrices
    if intrinsic:
        # Intrinsic case,
        # axes = ax1, ax2, ax3
        # angles = a, b, c
        # R =  R1(a) * R2(b) * R3(c)
        mode = 'intrinsic'

    else:
        # Extrinsic case,
        # axes = ax1, ax2, ax3
        # angles = a, b, c
        # R =  R3(c) * R2(b) * R1(a)
        mode = 'extrinsic'

    rotation_matrices = compose_rotation_matrices(elemental_rotations=elemental_rotations, mode=mode)

    return rotation_matrices.squeeze()
