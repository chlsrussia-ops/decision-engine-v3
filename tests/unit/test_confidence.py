from decision_engine_v3.engine.confidence import compute_confidence
from decision_engine_v3.models.data import EvidenceResult, SignalCleaningResult

def test_high_confidence():
    r = compute_confidence(EvidenceResult(evidence_score=0.8, comment_confidence=0.9, volume_confidence=0.8), SignalCleaningResult(uniqueness_score=0.95, clean_comment_count=30))
    assert r.confidence > 0.4

def test_low_evidence_caps_confidence():
    r = compute_confidence(EvidenceResult(evidence_score=0.2, comment_confidence=0.1, volume_confidence=0.1), SignalCleaningResult(uniqueness_score=0.3, clean_comment_count=3))
    assert r.confidence <= 0.40
    assert "low_evidence_cap" in r.penalties

def test_small_sample_penalty():
    r = compute_confidence(EvidenceResult(evidence_score=0.5, comment_confidence=0.5, volume_confidence=0.5), SignalCleaningResult(uniqueness_score=0.8, clean_comment_count=5))
    assert "small_sample" in r.penalties
