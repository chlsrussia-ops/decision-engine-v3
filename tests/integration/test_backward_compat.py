from decision_engine_v3.wrapper.integration import DecisionEngineWrapper
from decision_engine_v3.models.requests import LegacyExplorePayload
from decision_engine_v3.flags.config import FeatureFlags

def _payload():
    return LegacyExplorePayload(views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить","сколько стоит","хочу","беру","ссылку","артикул","нужно","заказать","цена","доставка","заказал","куплю","хочу подарок","где дешевле","доставкой"],
        total_comments=15, product_name="Compat Test")

def test_legacy_fields_always_present():
    r = DecisionEngineWrapper().evaluate_explore(_payload())
    assert "action" in r and isinstance(r["action"], str)
    assert "intent_score" in r and isinstance(r["intent_score"], (int, float))
    assert "viability" in r and isinstance(r["viability"], (int, float))
    assert "reasons" in r and isinstance(r["reasons"], list)

def test_v3_fields_present():
    r = DecisionEngineWrapper().evaluate_explore(_payload())
    assert r["engine_version"] == "v3"
    assert "confidence" in r
    assert "reason_codes" in r
    assert "red_flags" in r
    assert "decision_trace" in r

def test_all_flags_off_stable():
    flags = FeatureFlags(enable_signal_cleaning=False, enable_qualified_intent=False, enable_antiviral_v3=False, enable_marketplace_modifier_v3=False, enable_confidence_engine=False, enable_caution_status=False, enable_decision_trace=False, enable_reviewer_packet=False)
    r = DecisionEngineWrapper(flags).evaluate_explore(_payload())
    assert "action" in r
    assert "degraded" in r
    assert isinstance(r["degraded"], bool)
