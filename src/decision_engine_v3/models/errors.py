"""Domain errors."""

class FeatureFlagConfigError(Exception):
    """Raised when feature flag combination is invalid."""

class PayloadValidationError(Exception):
    """Raised when incoming payload is structurally invalid."""

class SerializationError(Exception):
    """Raised when response serialization fails unexpectedly."""
