from decision_engine_v3.engine.intent import compute_intent

def test_high_intent():
    r = compute_intent(["где купить этот товар", "сколько стоит"])
    assert r.high_intent_hits == 2
    assert r.qualified_intent > 0

def test_negative():
    r = compute_intent(["фигня полная", "развод", "хочу"])
    assert r.negative_hits == 2
    assert r.negative_rate > 0.5

def test_empty():
    r = compute_intent([])
    assert r.qualified_intent == 0.0
