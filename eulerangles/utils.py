from typing import List, Iterable, Union

class MetaData:
    """
    Metadata which can be associated with any object by inheritance
    Facilitates passing metadata between objects
    """

    def __init__(self, *args, **kwargs):
        # Initialise empty object and check for parent object
        if 'parent' in kwargs.keys():
            self.parent = kwargs['parent']
        else:
            self.parent = None

        # Initialise parameters from args, parents then kwargs.
        # Order is important here, args are empty by definition, try to fill from parent
        # then kwargs have highest priority (will overwrite definitions from parent)
        self._add_from_args(*args)
        self._fill_from_parent()
        self._add_from_kwargs(**kwargs)

    def _fill_from_obj(self, obj: object):
        # Check if any objects from args are currently unfilled attributes in this class
        # args = self.unfilled_attributes(args)

        # Check if object is a class with attributes
        if getattr(obj, '__dict__', None) is None:
            return

        # Get attribute names and values of object and unfilled attributes in current object
        obj_attributes = vars(obj)
        unfilled_attributes = self.unfilled_attribute_names

        # Set attributes in new object
        for attribute in unfilled_attributes:
            if attribute in obj_attributes.keys() and attribute != 'parent':
                setattr(self, attribute, obj_attributes[attribute])
        return

    def _fill_from_parent(self):
        # Return if parent object is None
        if self.parent is None:
            return

        # Try to fill unfilled attributes from parent object
        self._fill_from_obj(self.parent)
        return

    @property
    def _public_attribute_names(self) -> Iterable[str]:
        public_attribute_names = vars(self).keys()
        # vars(obj) does not return properties, it does return _property because that's where we store the actual value
        # remove '_' to fix list of attributes
        public_attribute_names = [remove_prefix(attribute, '_') for attribute in public_attribute_names]
        return public_attribute_names

    @property
    def unfilled_attribute_names(self) -> List[str]:
        """
        returns a list of attributes names for attributes which are currently None
        :return: unfilled_attributes
        """
        public_attributes = self._public_attribute_names
        unfilled_attributes = []

        for attribute in public_attributes:
            if getattr(self, attribute) is None:
                unfilled_attributes.append(attribute)

        return unfilled_attributes

    def add_metadata(self, parameter_name: str, value: object = None):
        """
        Adds a new piece of metadata to object, value of parameter defaults to None
        Will overwrite existing parameters
        :param parameter_name: name of parameter to be added
        :param value: default value to be given for the parameter
        """
        setattr(self, parameter_name, value)
        if value is None:
            self._fill_from_parent()
        return

    def has_metadata(self, attribute_name: str) -> bool:
        return self._attribute_exists(attribute_name)

    def _attribute_is_empty(self, attribute: str) -> Union[bool, None]:
        """
        returns True if attribute is None in this object
        returns None if attribute is not present
        :param attribute: attribute to check
        :return: bool or None
        """
        if self._attribute_exists(attribute):
            attribute = getattr(self, attribute)
            if attribute is None:
                return True
            return False
        return None

    def _attribute_is_filled(self, attribute: str) -> Union[bool, None]:
        """
        returns True if attribute is not None in this object
        returns None if attribute is not present
        not None is True hence extra specific checks
        :param attribute: attribute to check
        :return: bool or None
        """
        if self._attribute_is_empty(attribute):
            return not self._attribute_is_empty(attribute)
        if self._attribute_is_empty(attribute) is False:
            return not self._attribute_is_empty(attribute)
        return None

    def _attribute_exists(self, attribute: str) -> bool:
        """
        returns True if attribute exists in object else False
        :param attribute: attribute to check
        :return: bool
        """
        try:
            getattr(self, attribute)
            return True
        except AttributeError:
            return False

    def _add_from_args(self, *args):
        """
        Adds new empty parameters to a convention
        Does not overwrite existing parameters
        :param args: parameter names to add to the convention object
        """
        for arg in args:
            if isinstance(arg, str) and getattr(self, arg, None) is None:
                self.add_metadata(arg)
        return

    def _add_from_kwargs(self, **kwargs):
        """
        Adds parameters from keyword arguments, overwriting anything already in place in the convention
        :param kwargs: arguments to be overwritten in convention
        """
        for parameter_name, value in kwargs.items():
            self.add_metadata(parameter_name, value)
        return


def remove_prefix(s: str, prefix: str):
    if s.startswith(prefix):
        return s[len(prefix):]
    return s
