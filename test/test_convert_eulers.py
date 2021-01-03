from numpy.testing import assert_array_almost_equal

from eulerangles import convert_eulers

dynamo_eulers = [-47.2730, 1.1777, -132.3000]
relion_eulers = [137.7000, 1.1777, 42.7270]


def test_convert_eulers_dynamo_to_relion():
    result_eulers = convert_eulers(dynamo_eulers,
                                   source_meta='dynamo',
                                   target_meta='relion')
    assert_array_almost_equal(relion_eulers, result_eulers, decimal=5)


def test_convert_eulers_relion_to_dynamo():
    result_eulers = convert_eulers(relion_eulers,
                                   source_meta='relion',
                                   target_meta='dynamo')
    assert_array_almost_equal(dynamo_eulers, result_eulers, decimal=5)
