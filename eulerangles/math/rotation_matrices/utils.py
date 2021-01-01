import numpy as np


def invert_rotation_matrices(rotation_matrices: np.ndarray):
    """
    Invert rotation matrices by transposing the last two axes
    """
    return rotation_matrices.swapaxes(-1, -2)


