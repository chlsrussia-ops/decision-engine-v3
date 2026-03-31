from decision_engine_v3.engine.neutral_builders import *

def test_neutral_cleaning_conservative():
    r = neutral_cleaning()
    assert r.clean_comment_count == 0
    assert r.uniqueness_score == 0.5

def test_neutral_evidence_zero():
    r = neutral_evidence()
    assert r.evidence_score == 0.0

def test_neutral_antiviral_unknown():
    r = neutral_antiviral()
    assert r.status == "unknown"
    assert r.antiviral_score == 0.0

def test_neutral_confidence_zero():
    r = neutral_confidence()
    assert r.confidence == 0.0

def test_neutral_economics_unknown():
    r = neutral_economics()
    assert r.status == "unknown"
