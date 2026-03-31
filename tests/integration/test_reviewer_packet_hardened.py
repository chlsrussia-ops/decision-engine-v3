"""Test hardened reviewer packet."""
from decision_engine_v3.wrapper.reviewer_packet import build_reviewer_packet
from decision_engine_v3.models.data import Decision, ContentMetrics, EvidenceResult, AntiViralResult, EconomicsResult, ConfidenceResult
from decision_engine_v3.models.enums import Action

def test_focus_severity_ranked():
    d = Decision(action=Action.HOLD, red_flags=[])
    p = build_reviewer_packet(d, evidence=EvidenceResult(evidence_score=0.2), antiviral=AntiViralResult(antiviral_score=0.5), economics=EconomicsResult(status="fail"))
    # economics fail (10) > high antiviral (9) > weak evidence (7)
    assert p.review_focus[0] == "economics fail"
    assert p.review_focus[1] == "high antiviral"
    assert p.review_focus[2] == "weak evidence"

def test_degraded_checklist():
    d = Decision(action=Action.HOLD, degraded=True, degraded_modules=["intent", "confidence"])
    p = build_reviewer_packet(d)
    assert any("DEGRADED" in item for item in p.reviewer_checklist)
    assert any("intent" in item for item in p.reviewer_checklist)

def test_confidence_explanation_from_real_data():
    d = Decision(action=Action.HOLD, confidence=0.45)
    p = build_reviewer_packet(d, confidence=ConfidenceResult(confidence=0.45, components={"comment": 0.3, "volume": 0.2}, penalties=["small_sample"]))
    assert "0.45" in p.confidence_explanation
    assert "small_sample" in p.confidence_explanation

def test_packet_works_without_any_engine_results():
    d = Decision(action=Action.HOLD)
    p = build_reviewer_packet(d)
    assert p.recommendation == "HOLD"
    assert p.evidence_score == 0
    assert p.marketplace_summary["saturation"] == "unknown"
