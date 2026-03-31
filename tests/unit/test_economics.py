from decision_engine_v3.engine.economics import compute_economics
from decision_engine_v3.models.data import EconomicsPreview

def test_good_margin():
    r = compute_economics(EconomicsPreview(target_price=2000, landed_cost=500, platform_fee_pct=15, market_min_price=700))
    assert r.margin_ok
    assert r.estimated_margin_pct > 10

def test_bad_margin():
    r = compute_economics(EconomicsPreview(target_price=100, landed_cost=95, platform_fee_pct=15, market_min_price=50))
    assert not r.margin_ok
    assert r.status == "fail"

def test_landed_above_market():
    r = compute_economics(EconomicsPreview(target_price=1000, landed_cost=800, platform_fee_pct=15, market_min_price=600))
    assert r.landed_above_market_min

def test_no_economics():
    r = compute_economics(None)
    assert r.status == "unknown"
