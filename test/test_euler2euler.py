from numpy.testing import assert_array_almost_equal

from eulerangles import euler2euler
from eulerangles.utils import get_conversion_metadata


def test_euler2euler_dynamo2relion():
    dynamo_eulers = [-47.2730, 1.1777, -132.3000]
    relion_eulers = [137.7000, 1.1777, 42.7270]

    dynamo_meta = get_conversion_metadata('dynamo')
    relion_meta = get_conversion_metadata('relion')

    result_eulers = euler2euler(dynamo_eulers,
                                source_axes=dynamo_meta.axes,
                                source_intrinsic=dynamo_meta.intrinsic,
                                source_right_handed_rotation=dynamo_meta.right_handed_rotation,
                                target_axes=relion_meta.axes,
                                target_intrinsic=relion_meta.intrinsic,
                                target_right_handed_rotation=relion_meta.right_handed_rotation,
                                invert_matrix=False)

    assert_array_almost_equal(relion_eulers, result_eulers, decimal=5)
