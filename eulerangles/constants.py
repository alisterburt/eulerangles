from .base import ConversionMeta

euler_angle_metadata = {
    'relion': ConversionMeta(name='relion',
                             axes='zyz',
                             intrinsic=True,
                             right_handed_rotation=True,
                             active=False),

    'dynamo': ConversionMeta(name='dynamo',
                             axes='zxz',
                             intrinsic=False,
                             right_handed_rotation=True,
                             active=False),

    'warp': ConversionMeta(name='warp',
                           axes='ZYZ',
                           intrinsic=True,
                           right_handed_rotation=True,
                           active=False),

    'm': ConversionMeta(name='warp',
                        axes='ZYZ',
                        intrinsic=True,
                        right_handed_rotation=True,
                        active=False),
}
