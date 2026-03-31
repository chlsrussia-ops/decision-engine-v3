"""Contract snapshot tests — response shape must never change accidentally."""
from decision_engine_v3.wrapper.integration import DecisionEngineWrapper
from decision_engine_v3.models.requests import LegacyExplorePayload, LegacySellPayload
from decision_engine_v3.wrapper.serializer import REQUIRED_KEYS

def _explore_payload():
    return LegacyExplorePayload(
        views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить", "сколько стоит", "хочу", "беру", "ссылку",
                   "артикул", "нужно", "заказать", "цена", "доставка",
                   "заказал", "куплю", "хочу подарок", "где дешевле", "с доставкой"],
        total_comments=15, product_name="Snapshot Test",
    )

def test_explore_response_has_all_keys():
    w = DecisionEngineWrapper()
    r = w.evaluate_explore(_explore_payload())
    for key in REQUIRED_KEYS:
        assert key in r, f"Missing key: {key}"

def test_sell_response_has_all_keys():
    w = DecisionEngineWrapper()
    r = w.evaluate_sell(LegacySellPayload(orders=50, roi_pct=60, cvr_pct=2.0))
    for key in REQUIRED_KEYS:
        assert key in r, f"Missing key: {key}"

def test_response_engine_version():
    w = DecisionEngineWrapper()
    r = w.evaluate_explore(_explore_payload())
    assert r["engine_version"] == "v3"
