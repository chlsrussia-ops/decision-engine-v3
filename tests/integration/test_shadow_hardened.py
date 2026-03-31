"""Test shadow mode safety."""
from decision_engine_v3.wrapper.shadow import build_shadow_result, ShadowResult
from decision_engine_v3.models.data import Decision
from decision_engine_v3.models.enums import Action

def test_shadow_safe_on_broken_decision():
    """Shadow must not crash even with malformed decision."""
    class BrokenDecision:
        action = Action.HOLD
        intent_score = 0.0
        viability = 0.0
        confidence = 0.0
        reason_codes = []
        red_flag_codes = []
        trace = None  # broken
        caps = None   # broken
        degraded = False
        degraded_modules = []
    r = build_shadow_result("HOLD", 0.0, 0.0, BrokenDecision())
    assert isinstance(r, ShadowResult)
    assert r.shadow_error != ""  # error captured, not raised

def test_shadow_diff_explanation_readable():
    d = Decision(action=Action.TEST_PRODUCT, intent_score=0.5, viability=0.6, confidence=0.5)
    r = build_shadow_result("HOLD", 0.2, 0.3, d)
    assert r.action_changed is True
    assert "ACTION CHANGED" in r.decision_diff["explanation"]

def test_shadow_includes_degraded_info():
    d = Decision(action=Action.HOLD, degraded=True, degraded_modules=["intent"])
    r = build_shadow_result("HOLD", 0.0, 0.0, d)
    assert r.decision_diff.get("v3_degraded") is True
    assert "degraded" in r.decision_diff["explanation"]
