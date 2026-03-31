import pytest
from decision_engine_v3.flags.config import FeatureFlags

def test_valid_flags():
    f = FeatureFlags()
    assert f.validate() == []

def test_invalid_qualified_without_cleaning():
    f = FeatureFlags(enable_signal_cleaning=False, enable_qualified_intent=True)
    errors = f.validate()
    assert len(errors) > 0
    assert "qualified_intent requires signal_cleaning" in errors[0]

def test_validate_strict_raises():
    f = FeatureFlags(enable_signal_cleaning=False, enable_qualified_intent=True)
    with pytest.raises(ValueError):
        f.validate_strict()
