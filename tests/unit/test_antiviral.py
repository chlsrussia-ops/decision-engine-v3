from decision_engine_v3.engine.antiviral import compute_antiviral
from decision_engine_v3.models.data import ContentMetrics, IntentResult

def test_empty_viral():
    r = compute_antiviral(ContentMetrics(views=10000, ctr=0.002, save_rate=0.005), IntentResult(qualified_intent=0.01))
    assert r.empty_viral_score > 0

def test_clean():
    r = compute_antiviral(ContentMetrics(views=500, ctr=0.03, save_rate=0.04), IntentResult(qualified_intent=0.2))
    assert r.status == "clean"
