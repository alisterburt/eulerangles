from unittest import TestCase

from eulerangles.utils import MetaData


class MetaDataTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_instantiation()

    def test_instantiation(self):
        self.info = MetaData()
        self.assertIsInstance(self.info, MetaData)

    def test_add_metadata(self):
        self.info.add_metadata('param1')
        self.assertIs(self.info.param1, None)

        self.info.add_metadata('param2', 'not_empty')
        self.assertEqual(self.info.param2, 'not_empty')

    def test_add_from_args(self):
        self.info._add_from_args('param1', 'param2', 'param3')
        for arg in ('param1', 'param2', 'param3'):
            self.assertTrue(getattr(self.info, arg) is None)

    def test_add_from_kwargs(self):
        self.info._add_from_kwargs(param1='a', param2=2, param3={})
        for arg in ('param1', 'param2', 'param3'):
            self.assertTrue(getattr(self.info, arg) is not None)
            self.assertTrue(getattr(self.info, arg) in ('a', 2, {}))

    def make_parent(self):
        parent = TestParent()
        return parent

    def test_get_public_attribute_names(self):
        info = MetaData('empty_param')
        public_attributes = info._public_attribute_names
        self.assertIn('empty_param', public_attributes)

    def test_is_empty(self):
        info = MetaData('empty_param')
        self.assertTrue(info._attribute_is_empty('empty_param'))
        info.add_metadata('not_empty', 1)
        self.assertFalse(info._attribute_is_empty('not_empty'))

    def test_get_unfilled_attribute_names(self):
        info = MetaData('param1', 'param2', param3='not empty!')
        unfilled_attributes = info.unfilled_attribute_names
        attribute_check = [getattr(info, attribute) for attribute in ('param1', 'param2', 'param3')]
        self.assertEqual(attribute_check, [None, None, 'not empty!'])

    def test_from_parent(self):
        parent = self.make_parent()
        info = MetaData('param1', 'param2', parent=parent)  # not param3
        for arg in ('param1', 'param2'):
            self.assertTrue(getattr(info, arg) is not None)
            self.assertTrue(getattr(info, arg) in ('a', 2, {}))

        self.assertFalse(info.has_metadata('param3'))


class TestParent(MetaData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.param1 = 'a'
        self.param2 = 2
        self.param3 = {}
