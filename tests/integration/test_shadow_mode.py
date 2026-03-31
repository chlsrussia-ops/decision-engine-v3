from decision_engine_v3.wrapper.integration import DecisionEngineWrapper
from decision_engine_v3.models.requests import LegacyExplorePayload
from decision_engine_v3.flags.config import FeatureFlags

def _payload():
    return LegacyExplorePayload(views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить","сколько стоит","хочу","беру","ссылку","артикул","нужно","заказать","цена","доставка","заказал","куплю","подарок","дешевле","доставкой"],
        total_comments=15)

def test_shadow_present_when_enabled():
    w = DecisionEngineWrapper(FeatureFlags(enable_shadow_mode=True, enable_decision_trace=True))
    r = w.evaluate_explore(_payload(), v2_action="HOLD", v2_intent=0.3, v2_viability=0.2)
    assert "shadow" in r
    assert "v2_action" in r["shadow"]
    assert "v3_action" in r["shadow"]
    assert "decision_diff" in r["shadow"]

def test_shadow_absent_when_disabled():
    w = DecisionEngineWrapper(FeatureFlags(enable_shadow_mode=False))
    r = w.evaluate_explore(_payload())
    assert "shadow" not in r

def test_shadow_does_not_mutate_action():
    w = DecisionEngineWrapper(FeatureFlags(enable_shadow_mode=True, enable_decision_trace=True))
    r1 = w.evaluate_explore(_payload())
    r2 = w.evaluate_explore(_payload(), v2_action="SCALE", v2_intent=1.0, v2_viability=1.0)
    assert r1["action"] == r2["action"]  # shadow input must not change primary decision
