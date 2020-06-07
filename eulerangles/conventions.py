from .utils import MetaData


class Convention(MetaData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._replace_parent_attribute_names('convention')
        self._set_attribute_suffix('convention')


class AngleConvention(Convention):
    def __init__(self, units: str = None, positive_ccw: bool = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_parameter('units', units)
        self.add_parameter('positive_ccw', positive_ccw)

    @property
    def units(self):
        units = self.units.strip().lower()
        if units in ('degrees', 'degree', 'deg', 'd'):
            return 'degrees'
        elif units in ('radians', 'radian', 'rad', 'r'):
            return 'radians'
        raise ValueError(f"Could not parse {units} as 'degrees' or 'radians'")

    @property
    def positive_ccw(self):
        positive_ccw = self.positive_ccw()
        if isinstance(positive_ccw, bool):
            return positive_ccw
        elif isinstance(positive_ccw, str):
            if positive_ccw.strip().lower().startswith(('t', 'y')):
                return True
            elif positive_ccw.strip().lower().startswith(('f', 'n')):
                return False
        raise ValueError(f"Could not parse '{positive_ccw}' as True or False")


class EMRotationConvention(Convention):
    """
    Rotation conventions in electron microscopy single particle analysis and subtomogram averaging
    """

    def __init__(self, reference_frame: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_parameter('reference_frame', reference_frame)

    @property
    def get_reference_frame(self):
        assert isinstance(self.reference_frame, str)
        reference_frame = self.reference_frame.strip().lower()
        if reference_frame in ('rr', 'rotate_reference', 'reference', 'ref', 'r', 'rotate reference'):
            return 'rotate_reference'
        elif reference_frame in ('rp', 'rotate_particle', 'particle', 'p', 'rotate particle'):
            return 'rotate_particle'
        raise ValueError(f"Could not parse '{reference_frame}' as 'rotate_reference' or 'rotate_particle'")


class EulerAngleConvention(Convention, AngleConvention):
    def __init__(self, axes: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_parameter('axes', axes)

    @property
    def get_axes(self):
        assert isinstance(self.axes, str)
        axes = self.axes.strip().lower()
        if len(axes) == 3 and all([axis in ('x', 'y', 'z') for axes in axes]):
            return axes
        raise ValueError(f"Could not parse '{axes}' as a valid set of axes for Euler angles')


class EMEulerAngleConvention(EMRotationConvention, EulerAngleConvention):
    def __init__(self):





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
