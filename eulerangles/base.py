from dataclasses import dataclass

@dataclass
class EulerAngleConversionMeta:
    """
    A simple object holding metadata explaining how to interpret Euler angles in the context of
    density reconstruction from transmission electron microscopy data.
    """
    software: str
    axes: str
    intrinsic: bool
    positive_ccw: bool
    rotate_reference: bool


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
