from typing import List, Iterable, Union


class Info:
    def __init__(self, *args, **kwargs):
        # Initialise empty object
        self.parent = None
        self.parent_attribute_names = []
        self._add_parent_attribute_name('info')

        # Initialise parameters from args and kwargs
        self._add_from_args(*args)
        self._add_from_kwargs(**kwargs)
        self._fill_from_parent()

    def get_parent(self):
        """
        Returns the parent object the information is associated with
        :return: parent object
        """
        return self.parent

    def _fill_from_obj(self, obj: object):
        # Check if any objects from args are currently unfilled attributes in this class
        # args = self.unfilled_attributes(args)

        # Check if object is a class with attributes
        if getattr(obj, '__dict__', None) is None:
            return

        # Get attribute names and values of object and unfilled attributes in current object
        obj_attributes = vars(obj)
        unfilled_attributes = self.get_unfilled_attribute_names()

        # Set attributes in new object
        for attribute in unfilled_attributes:
            if attribute in obj_attributes.keys() and attribute != 'parent':
                setattr(self, attribute, obj_attributes[attribute])
        return

    def _fill_from_parent(self):
        # Get unfilled attribute names
        unfilled_attribute_names = self.get_unfilled_attribute_names()

        # Return if parent object is None
        if self.get_parent() is None:
            return

        # First try to fill from each of parent.parent_attribute name
        for attribute in self.parent_attribute_names:

            parent_info = getattr(self.parent, attribute, None)
            if parent_info is not None:
                self._fill_from_obj(parent_info)

        # Then try to fill from parent object itself (for compatibility)
        self._fill_from_obj(self.parent)
        return

    def get_public_attribute_names(self) -> Iterable[str]:
        return vars(self).keys()

    def get_unfilled_attribute_names(self) -> List[str]:
        """
        returns a list of attributes names for attributes which are currently None
        :return: unfilled_attributes
        """
        public_attributes = self.get_public_attribute_names()
        unfilled_attributes = []

        for attribute in public_attributes:
            if getattr(self, attribute) is None and attribute != 'parent_attribute_names':
                unfilled_attributes.append(attribute)

        return unfilled_attributes

    def add_parameter(self, name: str, value: object = None):
        """
        Adds a new parameter to a convention class, value of parameter defaults to None
        Will overwrite existing parameters
        :param name: name of parameter to be added
        :param value: default value to be given for the parameter
        """
        setattr(self, name, value)
        return

    def is_empty(self, attribute: str) -> Union[bool, None]:
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

    def is_filled(self, attribute: str) -> Union[bool, None]:
        """
        returns True if attribute is not None in this object
        returns None if attribute is not present
        not None is True hence extra specific checks
        :param attribute: attribute to check
        :return: bool or None
        """
        if self.is_empty(attribute):
            return not self.is_empty(attribute)
        if self.is_empty(attribute) is False:
            return not self.is_empty(attribute)
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
        except:
            return False

    def _add_from_args(self, *args):
        """
        Adds new empty parameters to a convention
        Does not overwrite existing parameters
        :param args: parameter names to add to the convention object
        """
        for arg in args:
            if isinstance(arg, str) and getattr(self, arg, None) is None:
                self.add_parameter(arg)
        return

    def _add_from_kwargs(self, **kwargs):
        """
        Adds parameters from keyword arguments, overwriting anything already in place in the convention
        :param kwargs: arguments to be overwritten in convention
        """
        for parameter_name, value in kwargs.items():
            self.add_parameter(parameter_name, value)
        return

    def _add_parent_attribute_name(self, parent_attribute_name: str):
        """
        Adds a name to the list of attributes to search in a parent object when filling information from the parent
        object
        :param parent_attribute_name: name of attribute to add
        :return:
        """
        self.parent_attribute_names.append(parent_attribute_name)
        return

    def _replace_parent_attribute_names(self, parent_attribute_names: Iterable[str]):
        if isinstance(parent_attribute_names, Iterable) and not isinstance(parent_attribute_names, str):
            setattr(self, 'parent_attribute_names', parent_attribute_names)
            return
        setattr(self, 'parent_attribute_names', [parent_attribute_names])
        return
