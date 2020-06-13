from .utils import MetaData


class Convention(MetaData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AngleConvention(Convention):
    """
    Convention for angles, provides attributes 'units' and 'positive_ccw'
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
        return self._units

    @units.setter
    def units(self, units: str):
        if units is None:
            self._units = None
            return

        elif units in ('degrees', 'degree', 'deg', 'd'):
            self._units = 'degrees'
            return

        elif units in ('radians', 'radian', 'rad', 'r'):
            self._units = 'radians'
            return

        raise ValueError(f"Could not parse {units} as 'degrees' or 'radians'")

    @property
    def positive_ccw(self):
        return self._positive_ccw

    @positive_ccw.setter
    def positive_ccw(self, positive_ccw: bool):
        if positive_ccw is None:
            self._positive_ccw = None
            return

        elif isinstance(positive_ccw, bool):
            self._positive_ccw = positive_ccw
            return

        elif isinstance(positive_ccw, str):
            if positive_ccw.strip().lower().startswith(('t', 'y')):
                self._positive_ccw = True
                return
            elif positive_ccw.strip().lower().startswith(('f', 'n')):
                self._positive_ccw = False
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
        return self._reference_frame

    @reference_frame.setter
    def reference_frame(self, reference_frame: str):
        if reference_frame is None:
            self._reference_frame = reference_frame
            return

        assert isinstance(reference_frame, str)

        reference_frame = reference_frame.strip().lower()
        if reference_frame in ('rr', 'rotate_reference', 'reference', 'ref', 'r', 'rotate reference'):
            self._reference_frame = 'rotate_reference'
            return

        elif reference_frame in ('rp', 'rotate_particle', 'particle', 'p', 'rotate particle'):
            self._reference_frame = 'rotate_particle'
            return

        raise ValueError(f"Could not parse '{reference_frame}' as 'rotate_reference' or 'rotate_particle'")


class EulerAngleConvention(AngleConvention):
    def __init__(self, axes: str = None, intrinsic: bool = None, extrinsic: bool = None, positive_ccw: bool = None,
                 *args, **kwargs):
        # Must set properties before calling super so that properties can be filled from parent objects
        self.axes = axes
        self.intrinsic = intrinsic
        self.extrinsic = extrinsic
        super().__init__(*args, **kwargs)
        # Set positive_ccw after call to init to override in case was filled by parent (already exists in
        # AngleConvention
        self.positive_ccw = positive_ccw

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, axes):
        if axes is None:
            self._axes = axes
            return

        assert isinstance(axes, str)
        axes = axes.strip().lower()

        if len(axes) == 3 and all([axis in ('x', 'y', 'z') for axis in axes]):
            self._axes = axes
            return

        raise ValueError(f"Could not parse '{axes}' as a valid set of axes for Euler angles")

    @property
    def intrinsic(self):
        return self._intrinsic

    @intrinsic.setter
    def intrinsic(self, is_intrinsic: bool):
        if is_intrinsic:
            self._set_intrinsic()
            return
        elif not is_intrinsic:
            self._set_extrinsic()
            return
        raise TypeError

    @property
    def extrinsic(self):
        return self._extrinsic

    @extrinsic.setter
    def extrinsic(self, is_extrinsic: bool):
        if is_extrinsic:
            self.intrinsic = False
        elif not is_extrinsic:
            self.intrinsic = True

    def _set_intrinsic(self):
        self._intrinsic = True
        self._extrinsic = False
        return

    def _set_extrinsic(self):
        self._extrinsic = True
        self._intrinsic = False
        return


class EMEulerAngleConvention(EMRotationConvention, EulerAngleConvention):
    def __init__(self, software: str = None, axes: str = None, reference_frame: str = None, intrinsic: bool = None,
                 extrinsic: bool = None,
                 positive_ccw: bool = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axes = axes
        self.reference_frame = reference_frame
        self.intrinsic = intrinsic
        self.extrinsic = extrinsic
        self.positive_ccw = positive_ccw
        self.software = software

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, software_name: str = None):
        if software_name is None:
            self._software = None
            return

        assert isinstance(software_name, str)
        self._software = software_name.strip().lower()
        return


class ElementalRotationMatrixConvention(Convention):
    def __init__(self, axis: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis = axis

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis: str):
        if axis is None:
            self._axis = None
            return
        assert isinstance(axis, str)
        axis = axis.strip().lower()
        if axis in ('x', 'y', 'z'):
            self._axis = axis
            return
        raise ValueError(f"Axis must be one of 'x', 'y' or 'z'")


euler_angle_conventions = {
    'relion': EMEulerAngleConvention(software='relion',
                                     axes='ZYZ',
                                     reference_frame='rotate_reference',
                                     positive_ccw=True,
                                     intrinsic=True),

    'dynamo': EMEulerAngleConvention(software='dynamo',
                                     axes='ZXZ',
                                     reference_frame='rotate_reference',
                                     positive_ccw=True,
                                     extrinsic=True),

    'warp': EMEulerAngleConvention(software='warp',
                                   axes='ZYZ',
                                   reference_frame='rotate_reference',
                                   positive_ccw=True,
                                   intrinsic=True),

    'm': EMEulerAngleConvention(software='warp',
                                axes='ZYZ',
                                reference_frame='rotate_reference',
                                positive_ccw=True,
                                intrinsic=True),

    'peet': EMEulerAngleConvention(software='peet',
                                   axes='zxz',
                                   reference_frame='rotate_reference',
                                   positive_ccw=True,
                                   intrinsic=True),

    'emclarity': EMEulerAngleConvention(software='emclarity',
                                        axes='zxz',
                                        reference_frame='rotate_particle',
                                        positive_ccw=True,
                                        intrinsic=True),
}


def get_convention(convention: str):
    """
    Gets EMEulerAngleConvention objects from their software package names
    :param convention:
    :return: euler angle convention
    """
    try:
        convention = convention.strip().lower()
        convention = euler_angle_conventions[convention]
        return convention

    except KeyError:
        raise NotImplementedError(f"Convention '{convention}' is not yet implemented, "
                                  f"please create your own EulerAngleConvention object")
