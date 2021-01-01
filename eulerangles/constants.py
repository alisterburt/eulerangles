from .base import ConversionMeta

euler_angle_metadata = {
    'relion': ConversionMeta(software='relion',
                             axes='zyz',
                             intrinsic=True,
                             right_handed_rotation=True,
                             active=False),

    'dynamo': ConversionMeta(software='dynamo',
                             axes='zxz',
                             intrinsic=False,
                             right_handed_rotation=True,
                             active=False),

    'warp': ConversionMeta(software='warp',
                           axes='ZYZ',
                           intrinsic=True,
                           right_handed_rotation=True,
                           active=False),

    'm': ConversionMeta(software='warp',
                        axes='ZYZ',
                        intrinsic=True,
                        right_handed_rotation=True,
                        active=False),
}
