from decision_engine_v3.wrapper.integration import DecisionEngineWrapper
from decision_engine_v3.models.requests import LegacyExplorePayload, LegacySellPayload

def test_wrapper_low_save_never_test():
    r = DecisionEngineWrapper().evaluate_explore(LegacyExplorePayload(views=5000, clicks=100, ctr=0.02, save_rate=0.005, saves=25, comments=["хочу"]*10, total_comments=10))
    assert r["action"] == "NEVER_TEST"

def test_wrapper_sell_scale():
    r = DecisionEngineWrapper().evaluate_sell(LegacySellPayload(orders=50, roi_pct=60, cvr_pct=2.0))
    assert r["action"] == "SCALE"

def test_wrapper_sell_pause():
    r = DecisionEngineWrapper().evaluate_sell(LegacySellPayload(orders=10, roi_pct=-40, cvr_pct=0.5))
    assert r["action"] == "PAUSE"

def test_wrapper_good_signal():
    r = DecisionEngineWrapper().evaluate_explore(LegacyExplorePayload(
        views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить","сколько стоит","хочу","беру","ссылку","артикул","нужно","заказать","цена","доставка","заказал","куплю","подарок","дешевле","доставкой"],
        total_comments=15))
    assert r["action"] in ("TEST_PRODUCT", "CAUTION")
