"""Flag validation utilities."""
from .config import FeatureFlags


def validate_flags(flags: FeatureFlags) -> list[str]:
    return flags.validate()


def safe_flags(**overrides) -> FeatureFlags:
    flags = FeatureFlags(**overrides)
    errors = flags.validate()
    if errors:
        raise ValueError(f"Invalid flags: {errors}")
    return flags
