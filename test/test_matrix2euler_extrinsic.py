from numpy.testing import assert_array_almost_equal

from eulerangles import euler2matrix, matrix2euler
from eulerangles.math.constants import valid_axes


def test_all_valid_axes():
    eulers = [10, 20, 30]
    for axes in valid_axes:
        rotation_matrix = euler2matrix(eulers,
                                       axes=axes,
                                       intrinsic=False,
                                       right_handed_rotation=True)

        result_eulers = matrix2euler(rotation_matrix,
                                     axes=axes,
                                     right_handed_rotation=True,
                                     intrinsic=False)
        result_rotation_matrix = euler2matrix(result_eulers,
                                              axes=axes,
                                              intrinsic=False,
                                              right_handed_rotation=True)

        assert_array_almost_equal(eulers, result_eulers)
        assert_array_almost_equal(rotation_matrix, result_rotation_matrix)
