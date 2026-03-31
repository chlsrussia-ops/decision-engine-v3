from decision_engine_v3.engine.caps import build_caps, apply_cap
from decision_engine_v3.models.data import EvidenceResult, AntiViralResult, ConfidenceResult, EconomicsResult
from decision_engine_v3.models.enums import Action, CapReasonCode

def test_evidence_cap():
    caps = build_caps(EvidenceResult(evidence_score=0.20), AntiViralResult(), ConfidenceResult(confidence=0.5), EconomicsResult())
    assert caps.max_allowed_action == Action.HOLD
    assert CapReasonCode.EVIDENCE_TOO_LOW in caps.reasons

def test_antiviral_hard_block():
    caps = build_caps(EvidenceResult(evidence_score=0.8), AntiViralResult(antiviral_score=0.85), ConfidenceResult(confidence=0.5), EconomicsResult())
    assert caps.max_allowed_action == Action.DISCARD

def test_apply_cap_downgrades():
    from decision_engine_v3.models.data import DecisionCaps
    caps = DecisionCaps(max_allowed_action=Action.HOLD)
    assert apply_cap(Action.TEST_PRODUCT, caps) == Action.HOLD

def test_apply_cap_no_change():
    from decision_engine_v3.models.data import DecisionCaps
    caps = DecisionCaps(max_allowed_action=Action.SCALE)
    assert apply_cap(Action.HOLD, caps) == Action.HOLD
