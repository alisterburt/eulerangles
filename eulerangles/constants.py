from .base import EMEulerAngleConvention

euler_angle_conventions = {
    'relion': EMEulerAngleConvention(software='relion',
                                     axes='zyz',
                                     intrinsic=True,
                                     positive_ccw=True,
                                     rotate_reference=False),

    'dynamo': EMEulerAngleConvention(software='dynamo',
                                     axes='zxz',
                                     intrinsic=False,
                                     positive_ccw=True,
                                     rotate_reference=False),

    'warp': EMEulerAngleConvention(software='warp',
                                   axes='ZYZ',
                                   intrinsic=True,
                                   positive_ccw=True,
                                   rotate_reference=False),

    'm': EMEulerAngleConvention(software='warp',
                                axes='ZYZ',
                                intrinsic=True,
                                positive_ccw=True,
                                rotate_reference=False),
}
