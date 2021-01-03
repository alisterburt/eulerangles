import numpy as np
from numpy.testing import assert_array_almost_equal

from eulerangles import matrix2euler
from eulerangles.math.constants import valid_axes
from eulerangles.utils import get_conversion_metadata

test_matrix_single = np.array([[-0.99985746, 0.00734648, -0.01520186],
                               [-0.00755692, -0.99987577, 0.01383262],
                               [-0.01509835, 0.01394553, 0.99978876]])
test_matrix_multiple = np.tile(test_matrix_single, (5, 1))


def test_matrix2euler_all_combinations():
    for matrix in (test_matrix_single, test_matrix_multiple):
        for axes in valid_axes:
            for intrinsic in (True, False):
                for positive_ccw in (True, False):
                    result = matrix2euler(matrix,
                                          axes=axes,
                                          intrinsic=True,
                                          right_handed_rotation=True)
                    assert result.shape[-1] == 3


def test_matrix2euler_dynamo():
    dynamo_matrix = np.array([[-0.0173, -0.5477, 0.8365],
                              [0.9012, -0.3709, -0.2241],
                              [0.4330, 0.7500, 0.5000]])
    dynamo_eulers = np.array([30, 60, 75])
    dynamo_meta = get_conversion_metadata('dynamo')

    result_eulers = matrix2euler(dynamo_matrix,
                                 axes=dynamo_meta.axes,
                                 intrinsic=dynamo_meta.intrinsic,
                                 right_handed_rotation=dynamo_meta.right_handed_rotation)

    assert_array_almost_equal(dynamo_eulers, result_eulers, decimal=2)


def test_matrix2euler_relion():
    relion_matrix = np.array([[-0.99985746, 0.00734648, -0.01520186],
                              [-0.00755692, -0.99987577, 0.01383262],
                              [-0.01509835, 0.01394553, 0.99978876]])
    relion_eulers = [137.7000, 1.1777, 42.7270]
    relion_meta = get_conversion_metadata('relion')

    result_eulers = matrix2euler(relion_matrix,
                                 axes=relion_meta.axes,
                                 intrinsic=relion_meta.intrinsic,
                                 right_handed_rotation=relion_meta.right_handed_rotation)

    assert_array_almost_equal(relion_eulers, result_eulers, decimal=4)
