from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_almost_equal

from eulerangles.eulers import EulerAngles


class EulersTest(TestCase):
    def assertEqual(self, *args, **kwargs):
        return assert_array_almost_equal(*args, **kwargs)

    def test_instantiation(self):
        ea = EulerAngle(np.zeros((9, 3)), 'relion')
        self.assertTrue(isinstance(ea, EulerAngles))
