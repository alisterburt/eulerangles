from .base import ConversionMeta

euler_angle_metadata = {
    'relion': ConversionMeta(software='relion',
                             axes='zyz',
                             intrinsic=True,
                             positive_ccw=True,
                             rotate_reference=False),

    'dynamo': ConversionMeta(software='dynamo',
                             axes='zxz',
                             intrinsic=False,
                             positive_ccw=True,
                             rotate_reference=False),

    'warp': ConversionMeta(software='warp',
                           axes='ZYZ',
                           intrinsic=True,
                           positive_ccw=True,
                           rotate_reference=False),

    'm': ConversionMeta(software='warp',
                        axes='ZYZ',
                        intrinsic=True,
                        positive_ccw=True,
                        rotate_reference=False),
}
