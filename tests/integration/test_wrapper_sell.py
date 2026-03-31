from decision_engine_v3.wrapper.integration import DecisionEngineWrapper
from decision_engine_v3.models.requests import LegacySellPayload

def test_sell_scale():
    w = DecisionEngineWrapper()
    r = w.evaluate_sell(LegacySellPayload(orders=50, roi_pct=60, cvr_pct=2.0))
    assert r["action"] == "SCALE"

def test_sell_pause():
    w = DecisionEngineWrapper()
    r = w.evaluate_sell(LegacySellPayload(orders=10, roi_pct=-40, cvr_pct=0.5))
    assert r["action"] == "PAUSE"

def test_sell_hold():
    w = DecisionEngineWrapper()
    r = w.evaluate_sell(LegacySellPayload(orders=2, roi_pct=100, cvr_pct=5.0))
    assert r["action"] == "HOLD"
