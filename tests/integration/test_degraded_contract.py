from decision_engine_v3.wrapper.serializer import serialize_decision, REQUIRED_KEYS
from decision_engine_v3.models.data import Decision
from decision_engine_v3.models.enums import Action

def test_degraded_decision_has_all_keys():
    d = Decision(action=Action.HOLD, degraded=True, degraded_modules=["intent", "evidence"], module_errors=["boom", "crash"])
    r = serialize_decision(d)
    for key in REQUIRED_KEYS:
        assert key in r
    assert r["degraded"] is True
    assert len(r["degraded_modules"]) == 2

def test_minimal_decision_stable():
    d = Decision()
    r = serialize_decision(d)
    assert r["action"] == "HOLD"
    assert r["engine_version"] == "v3"
    assert r["degraded"] is False
