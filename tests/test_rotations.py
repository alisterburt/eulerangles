from unittest import TestCase

# from eulerangles.rotations import Theta2RotationMatrix, RotX, RotY, RotZ
from eulerangles.rotations import Angles, RotationMatrix, ElementalRotationMatrix


class AnglesTest(TestCase):
    def test_instantiation(self):
        a = Angles([60, 90])
        self.assertIsInstance(a, Angles)
        self.assertTrue(a.units == None)
        self.assertTrue(a.positive_ccw == None)

        a = Angles([35, 45], units='degrees', positive_ccw=True)
        self.assertIsInstance(a, Angles)
        self.assertTrue(a.units == 'degrees')
        self.assertTrue(a.positive_ccw is True)

    def test_view(self):
        a = Angles([[60, 70, 80], [90, 100, 112], [1, 2, 3], [4, 5, 6]], units='degrees')
        b = a[1, :]
        self.assertTrue(b.units == 'degrees')


class RotationMatrixTest(TestCase):
    def test_instantiation(self):
        a = RotationMatrix()
        self.assertIsInstance(a, RotationMatrix)


class ElementalRotationMatrixTest(TestCase):
    def test_instantiation(self):
        a = ElementalRotationMatrix()
        self.assertIsInstance(a, ElementalRotationMatrix)
# class RotationsTest(TestCase):
#     def __init__(self, *args, **kwargs):
#         super(RotationsTest, self).__init__(*args, **kwargs)
#         self.x = np.asarray([1, 0, 0]).reshape(3, 1)
#         self.y = np.asarray([0, 1, 0]).reshape(3, 1)
#         self.z = np.asarray([0, 0, 1]).reshape(3, 1)
#
#     def assertEqual(self, *args, **kwargs):
#         return assert_array_almost_equal(*args, **kwargs)
#
#     def test_Theta2RotationMatrix_x(self):
#         rotation_matrix = Theta2RotationMatrix(90, 'x').get_rotation_matrix()
#         result = rotation_matrix @ self.x
#         self.assertEqual(result, self.x)
#
#         result = rotation_matrix @ self.y
#         self.assertEqual(result, self.z)
#
#         result = rotation_matrix @ self.z
#         self.assertEqual(result, -self.y)
#
#     def test_Theta2RotationMatrix_y(self):
#         rotation_matrix = Theta2RotationMatrix(90, 'y').get_rotation_matrix()
#         result = rotation_matrix @ self.x
#         self.assertEqual(result, -self.z)
#
#         result = rotation_matrix @ self.y
#         self.assertEqual(result, self.y)
#
#         result = rotation_matrix @ self.z
#         self.assertEqual(result, self.x)
#
#     def test_Theta2RotationMatrix_z(self):
#         rotation_matrix = Theta2RotationMatrix(90, 'z').get_rotation_matrix()
#         result = rotation_matrix @ self.x
#         self.assertEqual(result, self.y)
#
#         result = rotation_matrix @ self.y
#         self.assertEqual(result, -self.x)
#
#         result = rotation_matrix @ self.z
#         self.assertEqual(result, self.z)
#
#     def test_RotationMatrix(self):
#         result = RotationMatrix(theta=90, axis='x') @ self.x
#         self.assertEqual(result, self.x)
#
#         result = RotationMatrix(theta=90, axis='y') @ self.x
#         self.assertEqual(result, -self.z)
#
#         result = RotationMatrix(theta=90, axis='z') @ self.x
#         self.assertEqual(result, self.y)
#
#     def test_RotZ(self):
#         result = RotZ(90) @ self.x
#         self.assertEqual(result, self.y)
#
#     def test_RotY(self):
#         result = RotY(90) @ self.x
#         self.assertEqual(result, -self.z)
#
#     def test_RotX(self):
#         result = RotX(90) @ self.x
#         self.assertEqual(result, self.x)
