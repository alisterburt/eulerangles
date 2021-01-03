from .constants import euler_angle_metadata


def get_conversion_metadata(convention):
    """
    Attempts to retrieve ConversionMeta objects from a given software package name
    """
    try:
        convention = convention.strip().lower()
        convention = euler_angle_metadata[convention]
        return convention

    except KeyError:
        raise NotImplementedError(f"Convention '{convention}' is not yet implemented, "
                                  f"please create your own EulerAngleConvention object")
