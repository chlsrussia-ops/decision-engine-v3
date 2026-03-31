from decision_engine_v3.adapters.validation import validate_explore_payload, validate_sell_payload
from decision_engine_v3.models.requests import LegacyExplorePayload, LegacySellPayload

def test_valid_payload():
    errors = validate_explore_payload(LegacyExplorePayload(views=1000, clicks=20))
    assert errors == []

def test_negative_views():
    errors = validate_explore_payload(LegacyExplorePayload(views=-1))
    assert "views cannot be negative" in errors

def test_negative_clicks():
    errors = validate_explore_payload(LegacyExplorePayload(clicks=-5))
    assert "clicks cannot be negative" in errors

def test_sell_negative_orders():
    errors = validate_sell_payload(LegacySellPayload(orders=-1))
    assert "orders cannot be negative" in errors
