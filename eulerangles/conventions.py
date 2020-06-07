from .utils import MetaData


class Convention(MetaData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AngleConvention(Convention):
    """
    Convention for angles, provides attributs 'units' and 'positive_ccw'
    """

    def __init__(self, units: str = None, positive_ccw: bool = None, *args, **kwargs):
        """

        :param units: 'degrees' or 'radians'
        :param positive_ccw: do positive angles describe clockwise rotations?
        """
        self.units = units
        self.positive_ccw = positive_ccw
        super().__init__(*args, **kwargs)

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, units: str):
        units = self.units.strip().lower()
        if units in ('degrees', 'degree', 'deg', 'd'):
            self.__units = 'degrees'
            return
        elif units in ('radians', 'radian', 'rad', 'r'):
            self.__units = 'radians'
            return
        raise ValueError(f"Could not parse {units} as 'degrees' or 'radians'")

    @property
    def positive_ccw(self):
        return self.__positive_ccw

    @positive_ccw.setter
    def positive_ccw(self, positive_ccw: bool):
        positive_ccw = self.positive_ccw
        if isinstance(positive_ccw, bool):
            self.__positive_ccw = positive_ccw
            return
        elif isinstance(positive_ccw, str):
            if positive_ccw.strip().lower().startswith(('t', 'y')):
                self.__positive_ccw = True
                return
            elif positive_ccw.strip().lower().startswith(('f', 'n')):
                self.__positive_ccw = False
                return
        raise ValueError(f"Could not parse '{positive_ccw}' as True or False")


class RotationConvention(Convention):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EMRotationConvention(RotationConvention):
    """
    Rotation conventions in electron microscopy single particle analysis and subtomogram averaging
    """

    def __init__(self, reference_frame: str = None, *args, **kwargs):
        self.reference_frame = reference_frame
        super().__init__(*args, **kwargs)

    @property
    def reference_frame(self):
        return self.__reference_frame

    @reference_frame.setter
    def reference_frame(self, reference_frame: str):
        assert isinstance(self.reference_frame, str)
        reference_frame = self.reference_frame.strip().lower()
        if reference_frame in ('rr', 'rotate_reference', 'reference', 'ref', 'r', 'rotate reference'):
            self.__reference_frame = 'rotate_reference'
            return
        elif reference_frame in ('rp', 'rotate_particle', 'particle', 'p', 'rotate particle'):
            self.__reference_frame = 'rotate_particle'
            return
        raise ValueError(f"Could not parse '{reference_frame}' as 'rotate_reference' or 'rotate_particle'")


class EulerAngleConvention(AngleConvention):
    def __init__(self, axes: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axes = axes

    @property
    def axes(self):
        return self.__axes

    @axes.setter
    def axes(self):
        assert isinstance(self.axes, str)
        axes = self.axes.strip().lower()
        if len(axes) == 3 and all([axis in ('x', 'y', 'z') for axis in axes]):
            self.__axes = axes
        raise ValueError(f"Could not parse '{axes}' as a valid set of axes for Euler angles")


class EMEulerAngleConvention(EMRotationConvention, EulerAngleConvention):
    def __init__(self, *args, **kwargs):
        super(EMRotationConvention).__init__(*args, **kwargs)
        super(EulerAngleConvention).__init__(*args, **kwargs)





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
