from decision_engine_v3.engine.marketplace import compute_marketplace
from decision_engine_v3.models.data import MarketplaceMetrics

def test_no_marketplace():
    r = compute_marketplace(None)
    assert r.saturation_state == "unknown"
    assert r.block is False

def test_emerging_market():
    r = compute_marketplace(MarketplaceMetrics(competitors=10, avg_price=1000, min_price=500, max_price=1500, avg_reviews=5, top_seller_revenue_estimate=20000))
    assert r.saturation_state == "emerging"

def test_dead_market():
    r = compute_marketplace(MarketplaceMetrics(competitors=250, avg_price=100, min_price=90, max_price=110, avg_reviews=500, top_seller_revenue_estimate=5000))
    assert r.saturation_state == "dead"
    assert r.viability_adjustment < 0

def test_marketplace_never_upgrades():
    """Marketplace can only reduce or add caution, never upgrade."""
    r = compute_marketplace(MarketplaceMetrics(competitors=5, avg_price=2000, min_price=1000, max_price=3000, avg_reviews=100, top_seller_revenue_estimate=100000))
    assert r.viability_adjustment <= 0 or r.viability_adjustment == 0.0
