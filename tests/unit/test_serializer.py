from decision_engine_v3.wrapper.serializer import serialize_decision, validate_response_schema, REQUIRED_KEYS
from decision_engine_v3.models.data import Decision

def test_stable_keys():
    d = Decision()
    r = serialize_decision(d)
    missing = validate_response_schema(r)
    assert missing == [], f"Missing keys: {missing}"

def test_all_required_keys_present():
    d = Decision()
    r = serialize_decision(d)
    for key in REQUIRED_KEYS:
        assert key in r, f"Missing: {key}"

def test_degraded_fields_always_present():
    d = Decision()
    r = serialize_decision(d)
    assert isinstance(r["degraded"], bool)
    assert isinstance(r["degraded_modules"], list)
    assert isinstance(r["module_errors"], list)
