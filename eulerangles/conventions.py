# from .eulers import EulerAngleConvention
# from .rotations import axis_check


class Convention:
    def __init__(self, parent: object = None, *args, **kwargs):
        self.parent = parent
        self.from_parent(*args)
        self._add_from_args(*args)
        self._add_from_kwargs(**kwargs)

    def get_parent(self):
        """
        Returns the parent object the convention is associated with
        :return: parent object
        """
        return self.parent

    def from_parent(self, *args):
        # First try to fill from convention object in parent
        parent_convention = getattr(self.parent, 'convention', None)
        if parent_convention is not None:
            self.from_obj(parent_convention, args)

        # Then try to fill from parent object itself (for compatibility)
        self.from_obj(args)
        return

    def from_obj(self, obj: object, *args):
        # Check if any objects from args are currently unfilled attributes
        args = self.unfilled_attributes(args)

        # Check if object is a class with attributes
        if getattr(obj, '__dict__', None) is None:
            return

        # Get attribute names and values of object
        obj_attributes = vars(obj)

        # Set attributes in new object
        for arg in args:
            current_attribute = getattr(self, arg, None)
            if arg in obj_attributes.keys() and current_attribute is None:
                self.__setattr__(arg, obj_attributes[arg])
        return

    def unfilled_attributes(self, *args):
        unfilled_attributes = list(filter(None, [getattr(self, arg, None)
                                                 for arg in args
                                                 if isinstance(arg, str)]))
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
#
#
# class RotationMatrixConvention(Convention):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def get_parent(self):
#         return self.parent
#
#
# class ElementalRotationMatrixConvention(RotationMatrixConvention):
#     def __init__(self, axis: str = None, **kwargs):
#         super().__init__(**kwargs)
#         self.axis = self.parse_axis(axis)
#
#     @staticmethod
#     def parse_axis(self, axis):
#         if axis.strip().lower() in ('x', 'y', 'z'):
#             return axis.strip.lower()
#         raise ValueError(f"axis {axis} could not be parsed as 'x', 'y' or 'z'")
#
#
# class EulerAngleRotationMatrixConvention(RotationMatrixConvention):
#     def __init__(self, axes: str = None, reference_frame: str = None,
#                  euler_angle_convention: EulerAngleConvention = None, **kwargs):
#         super().__init__(**kwargs)
#         if euler_angle_convention is not None:
#             self.from_euler_angle_convention(euler_angle_convention)
#         elif axes is not None and reference_frame is not None:
#             self.axes = self.parse_axes(axes)
#             self.reference_frame = self.parse_reference_frame(reference_frame)
#
#     @staticmethod
#     def parse_axes(self, axes: str):
#         axes = axes.strip().lower()
#         if (len(axes) == 3 and
#             all([axis_check(axis) for axis in axes]) and
#             not any(a == b for a, b in zip(axes, axes[1:]))
#             ):
#             return axes
#         raise ValueError(f"Could not parse {axes} as three elemental rotation axes which make valid euler angles")
#
#     @staticmethod
#     def parse_reference_frame(self, reference_frame: str):
#         reference_frame = reference_frame.strip().replace('_', ' ').lower()
#         if reference_frame in ('rotate reference', 'rr', 'rotref'):
#             return reference_frame
#         elif reference_frame in ('rotate particle', 'rp', 'rotpart'):
#             return reference_frame
#         raise ValueError(f"Could not parse {reference_frame} as 'rotate reference' or 'rotate particle'")
#
#     def from_euler_angle_convention(self, euler_angle_convention: EulerAngleConvention):
#         axes = self.parse_axes(euler_angle_convention.axes)
#         reference_frame = self.parse_reference_frame(euler_angle_convention.reference_frame)
#         self.__setattr__('axes', axes)
#         self.__setattr__('reference_frame', reference_frame)
#
#
# EulerAngleConventions = {
#     'relion': EulerAngleConvention('relion', 'ZYZ', 'rotate_reference', True, True),
#     'dynamo': EulerAngleConvention('dynamo', 'ZXZ', 'rotate_reference', False, True),
# }
