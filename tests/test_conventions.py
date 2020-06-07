from unittest import TestCase

from eulerangles.conventions import Convention


class ConventionTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_instantiation()

    def test_instantiation(self):
        self.convention = Convention()
        self.assertIsInstance(self.convention, Convention)


