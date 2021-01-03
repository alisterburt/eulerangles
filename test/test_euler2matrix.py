import numpy as np
from numpy.testing import assert_array_almost_equal
import pytest

from eulerangles import euler2matrix
from eulerangles.utils import get_conversion_metadata
from eulerangles.math.constants import valid_axes

test_eulers_single = [10, 20, 30]
test_eulers_multiple = np.arange(15).reshape((5, 3))


def test_euler2matrix_all_combinations():
    eulers = (test_eulers_single, test_eulers_multiple)
    for eulers in eulers:
        for axes in valid_axes:
            for intrinsic in (True, False):
                for right_handed_rotation in (True, False):
                    matrices = euler2matrix(eulers,
                                            axes=axes,
                                            intrinsic=intrinsic,
                                            right_handed_rotation=right_handed_rotation)
                    assert matrices.shape[-1] == 3
                    assert matrices.shape[-2] == 3


def test_euler2matrix_dynamo():
    dynamo_eulers = np.array([30, 60, 75])
    dynamo_matrix = np.array([[-0.0173, -0.5477, 0.8365],
                              [0.9012, -0.3709, -0.2241],
                              [0.4330, 0.7500, 0.5000]])
    dynamo_meta = get_conversion_metadata('dynamo')

    result_matrix = euler2matrix(dynamo_eulers,
                                 axes=dynamo_meta.axes,
                                 intrinsic=dynamo_meta.intrinsic,
                                 right_handed_rotation=dynamo_meta.right_handed_rotation)

    assert_array_almost_equal(dynamo_matrix, result_matrix, decimal=4)


def test_euler2matrix_relion():
    relion_eulers = [137.7000, 1.1777, 42.7270]
    relion_matrix = np.array([[-0.99985746, 0.00734648, -0.01520186],
                              [-0.00755692, -0.99987577, 0.01383262],
                              [-0.01509835, 0.01394553, 0.99978876]])
    relion_meta = get_conversion_metadata('relion')

    result_matrix = euler2matrix(relion_eulers,
                                 axes=relion_meta.axes,
                                 intrinsic=relion_meta.intrinsic,
                                 right_handed_rotation=relion_meta.right_handed_rotation)

    assert_array_almost_equal(relion_matrix, result_matrix, decimal=4)
