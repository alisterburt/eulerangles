from unittest import TestCase

from eulerangles.conventions import Convention


class ConventionTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_instantiation()

    def test_instantiation(self):
        self.convention = Convention()
        self.assertIsInstance(self.convention, Convention)

    def test_add_parameter(self):
        self.convention.add_parameter('param1')
        self.assertIs(self.convention.param1, None)

        self.convention.add_parameter('param2', 'not_empty')
        self.assertEqual(self.convention.param2, 'not_empty')

    def test_add_from_args(self):
        self.convention._add_from_args('param1', 'param2', 'param3')
        for arg in ('param1', 'param2', 'param3'):
            self.assertTrue(getattr(self.convention, arg) is None)

    def test_add_from_kwargs(self):
        self.convention._add_from_kwargs(param1='a', param2=2, param3={})
        for arg in ('param1', 'param2', 'param3'):
            self.assertTrue(getattr(self.convention, arg) is not None)
            self.assertTrue(getattr(self.convention, arg) in ('a', 2, {}))

    def make_parent(self):
        class TestParent:
            def __init__(self):
                convention = Convention(param1='a', param2=2, param3={})
                self.convention = convention

        return TestParent()

    def test_from_parent(self):
        parent = self.make_parent()
        self.convention = Convention(parent, 'param1', 'param2')  # not param3
        for arg in ('param1', 'param2'):
            self.assertTrue(getattr(self.convention, arg) is not None)
            self.assertTrue(getattr(self.convention, arg) in ('a', 2, {}))

        self.assertFalse(getattr(self.convention, 'param3', None) is None)
