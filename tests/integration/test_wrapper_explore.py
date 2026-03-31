from decision_engine_v3.wrapper.integration import DecisionEngineWrapper
from decision_engine_v3.models.requests import LegacyExplorePayload
from decision_engine_v3.flags.config import FeatureFlags

def _good_payload() -> LegacyExplorePayload:
    return LegacyExplorePayload(
        views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить", "сколько стоит", "хочу такой", "беру", "ссылку дай",
                   "артикул", "нужно", "как заказать", "цена какая", "доставка есть",
                   "заказал", "куплю", "хочу на подарок", "где купить дешевле", "сколько с доставкой"],
        total_comments=15, likes=200, shares=30,
        product_name="Test Widget",
    )

def test_backward_compat_keys():
    w = DecisionEngineWrapper()
    r = w.evaluate_explore(_good_payload())
    assert "action" in r
    assert "intent_score" in r
    assert "viability" in r
    assert "reasons" in r
    assert "engine_version" in r
    assert r["engine_version"] == "v3"

def test_degraded_field_present():
    w = DecisionEngineWrapper()
    r = w.evaluate_explore(_good_payload())
    assert "degraded" in r
    assert "degraded_modules" in r
    assert isinstance(r["degraded"], bool)

def test_reviewer_packet_present():
    w = DecisionEngineWrapper(FeatureFlags(enable_reviewer_packet=True))
    r = w.evaluate_explore(_good_payload())
    assert "reviewer_packet" in r
    assert "recommendation" in r["reviewer_packet"]
    assert "reviewer_checklist" in r["reviewer_packet"]

def test_shadow_mode():
    w = DecisionEngineWrapper(FeatureFlags(enable_shadow_mode=True, enable_decision_trace=True))
    r = w.evaluate_explore(_good_payload(), v2_action="HOLD", v2_intent=0.5, v2_viability=0.3)
    assert "shadow" in r
    assert "v2_action" in r["shadow"]
    assert "v3_action" in r["shadow"]
    assert "action_changed" in r["shadow"]
    assert "decision_diff" in r["shadow"]

def test_disabled_flags_stable_schema():
    flags = FeatureFlags(enable_signal_cleaning=False, enable_qualified_intent=False, enable_antiviral_v3=False, enable_marketplace_modifier_v3=False, enable_confidence_engine=False, enable_caution_status=False)
    w = DecisionEngineWrapper(flags)
    r = w.evaluate_explore(_good_payload())
    assert "action" in r
    assert "decision_trace" in r
    assert isinstance(r["degraded"], bool)
