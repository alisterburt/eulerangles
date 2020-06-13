from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_almost_equal

from eulerangles.conventions import euler_angle_conventions
from eulerangles.conversions import euler2matrix, matrix2euler


class ConversionTest(TestCase):
    def assertEqual(self, *args, **kwargs):
        return assert_array_almost_equal(*args, **kwargs)

    def test_dynamo_eulers2matrix(self):
        dynamo_eulers = [30, 60, 75]
        dynamo_matrix = np.asarray([[-0.0173, -0.5477, 0.8365],
                                    [0.9012, -0.3709, -0.2241],
                                    [0.4330, 0.7500, 0.5000]])
        c = euler_angle_conventions['dynamo']
        matrix = euler2matrix(dynamo_eulers, c.axes, c.intrinsic, c.extrinsic, c.positive_ccw)
        self.assertEqual(dynamo_matrix, matrix, decimal=4)

    def test_relion_eulers2matrix(self):
        # test_dynamo_eulers2matrix works
        # This is a known equivalent euler pair in the two conventions
        # they should give the same rotation matrix
        dynamo_eulers = [-47.2730, 1.1777, -132.3000]
        relion_eulers = [137.7000, 1.1777, 42.7270]
        dc = euler_angle_conventions['dynamo']
        rc = euler_angle_conventions['relion']
        dynamo_matrix = euler2matrix(dynamo_eulers, dc.axes, dc.intrinsic, dc.extrinsic, dc.positive_ccw)
        relion_matrix = euler2matrix(relion_eulers, rc.axes, rc.intrinsic, rc.extrinsic, rc.positive_ccw)
        self.assertEqual(dynamo_matrix, relion_matrix, decimal=4)

    def test_dynamo_matrix2euler(self):
        dynamo_eulers = [30, 60, 75]
        dynamo_matrix = np.asarray([[-0.0173, -0.5477, 0.8365],
                                    [0.9012, -0.3709, -0.2241],
                                    [0.4330, 0.7500, 0.5000]])
        c = euler_angle_conventions['dynamo']
        eulers = matrix2euler(dynamo_matrix, c.axes, c.positive_ccw, c.intrinsic, c.extrinsic)
        self.assertEqual(dynamo_eulers, eulers, decimal=2)

    def test_relion_matrix2euler(self):
        c = euler_angle_conventions['relion']
        relion_eulers = [137.7000, 1.1777, 42.7270]
        relion_matrix = euler2matrix(relion_eulers, c.axes, c.intrinsic, c.extrinsic, c.positive_ccw)
        eulers = matrix2euler(relion_matrix, c.axes, c.positive_ccw, c.intrinsic, c.extrinsic)
        # self.assertEqual(relion_eulers, eulers, decimal=2) # commented out because eulers can be degenerate
        matrix = euler2matrix(eulers, c.axes, c.intrinsic, c.extrinsic, c.positive_ccw)
        self.assertEqual(relion_matrix, matrix)
