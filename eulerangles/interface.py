from typing import Union

import numpy as np
from .base import ConversionMeta
from .math.eulers_to_eulers import euler2euler
from .utils import get_conversion_metadata


def convert_eulers(euler_angles: np.ndarray,
                   source_meta: Union[ConversionMeta, str],
                   target_meta: Union[ConversionMeta, str]):
    """
    Convert Euler angles defined according to one 'convention' into Euler angles defined
    according to another.

    Parameters
    ----------
    euler_angles : (n, 3) or (3,) array of float
        Euler angles to be converted

    source_meta : ConversionMeta or str
        metadata defining how to interpret the euler angles or a string with the name of a
        software package

    target_meta : ConversionMeta or str
        metadata defining how to generate euler angles or a string with the name of a software
        package

    Returns
    -------
    euler_angles : (n, 3) or (3,) array of float
        Euler angles resulting from conversion
    """
    # Attempt to get appropriate conversion metadata if a software package name is provided
    if isinstance(source_meta, str):
        source_meta = get_conversion_metadata(source_meta)
    if isinstance(target_meta, str):
        target_meta = get_conversion_metadata(target_meta)

    # Check if desired transformation is of the same type as the input Eulers
    if source_meta.active != target_meta.active:
        invert_matrix = True
    else:
        invert_matrix = False

    # Convert euler angles according to metadata
    final_eulers = euler2euler(euler_angles,
                               source_axes=source_meta.axes,
                               source_intrinsic=source_meta.intrinsic,
                               source_right_handed_rotation=source_meta.right_handed_rotation,
                               target_axes=target_meta.axes,
                               target_intrinsic=target_meta.intrinsic,
                               target_right_handed_rotation=target_meta.right_handed_rotation,
                               invert_matrix=invert_matrix)

    return final_eulers

