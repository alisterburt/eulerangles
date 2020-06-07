from unittest import TestCase

from eulerangles.conventions import Convention, EMEulerAngleConvention


class ConventionTest(TestCase):
    def test_instantiation(self):
        convention = Convention()
        self.assertIsInstance(convention, Convention)

    def test_EMEulerAngleConvention(self):
        convention = EMEulerAngleConvention()
        self.assertIsInstance(convention, EMEulerAngleConvention)
