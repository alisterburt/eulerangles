from dataclasses import dataclass


@dataclass
class ConversionMeta:
    """
    A simple object holding metadata explaining how to interpret Euler angles in the context of
    density reconstruction from transmission electron microscopy data.

    software: str
        the name of the software package
    axes: str
        a valid non-sequential sequence of axes e.g. 'zxz', 'yxz'
    intrinsic: bool
        True - the euler angles represent intrinsic rotations, the coordinate system moves with
        the rotating rigid body
        False - the euler angles represent extrinsic rotations, the rigid body rotates with
        respect to a fixed coordinate system
    positive_ccw: bool
        True - the euler angles represent right hand rotations in a right handed coordinate system
        False - the euler angles represent left hand rotations in a right handed coordinate system
    rotate_reference: bool
        True - the euler angles represent the rotation aligning a reference coordinate system
        with an object
        False - the euler angles represent the inverse rotation
        this property is compared between EulerAngleConversionMeta objects when deciding whether
        or not to invert rotation matrices derived from euler angles for conversion
    """
    software: str
    axes: str
    intrinsic: bool
    positive_ccw: bool
    rotate_reference: bool


