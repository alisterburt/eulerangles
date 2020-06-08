from unittest import TestCase

from eulerangles.conventions import Convention, AngleConvention, EMEulerAngleConvention


class ConventionTest(TestCase):
    def test_instantiation(self):
        convention = Convention()
        self.assertIsInstance(convention, Convention)

    def test_AngleConvention(self):
        convention = AngleConvention()
        self.assertIsInstance(convention, AngleConvention)

    def test_EMEulerAngleConvention(self):
        convention = EMEulerAngleConvention()
        self.assertIsInstance(convention, EMEulerAngleConvention)
        self.assertTrue(convention.has_metadata('axes'))
        self.assertTrue(convention.has_metadata('positive_ccw'))

    def test_EMEulerAngleConvention_w_params(self):
        convention = EMEulerAngleConvention(axes='zxz', reference_frame='rotate_particle')
        self.assertTrue(convention.has_metadata('reference_frame'))
        self.assertEqual(convention.axes, 'zxz')

    def test_from_parent(self):
        a = AngleConvention(positive_ccw=True)
        e = EMEulerAngleConvention(axes='ZXZ', reference_frame='rotate_reference', intrinsic=True, parent=a)
        # if e is correctly filled from parent, positive_ccw will not be empty
        self.assertTrue(None not in e.unfilled_attribute_names)
