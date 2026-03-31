from decision_engine_v3.engine.viability import compute_viability
from decision_engine_v3.models.data import ContentMetrics, IntentResult, EvidenceResult, AntiViralResult

def test_high_viability():
    r = compute_viability(ContentMetrics(ctr=0.03, save_rate=0.04, clicks=60, saves=120), IntentResult(qualified_intent=0.25), EvidenceResult(evidence_score=0.7, volume_confidence=0.8), AntiViralResult())
    assert r.viability > 0.3

def test_weak_evidence_caps():
    r = compute_viability(ContentMetrics(ctr=0.03, save_rate=0.04, clicks=60, saves=120), IntentResult(qualified_intent=0.25), EvidenceResult(evidence_score=0.20), AntiViralResult())
    assert r.viability <= 0.30
    assert "weak_evidence_cap" in r.caps_applied

def test_false_viral_caps():
    r = compute_viability(ContentMetrics(ctr=0.03, save_rate=0.04, clicks=60, saves=120), IntentResult(qualified_intent=0.25), EvidenceResult(evidence_score=0.7), AntiViralResult(false_viral_score=0.6))
    assert "false_viral_cap" in r.caps_applied
