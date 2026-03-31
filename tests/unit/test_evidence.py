from decision_engine_v3.engine.evidence import compute_evidence
from decision_engine_v3.models.data import ContentMetrics

def test_strong_evidence():
    r = compute_evidence(ContentMetrics(views=5000, clicks=100, total_comments=30))
    assert r.evidence_score > 0.5

def test_weak_evidence():
    r = compute_evidence(ContentMetrics(views=100, clicks=2, total_comments=3))
    assert r.evidence_score < 0.35
