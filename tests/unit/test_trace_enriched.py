"""Test enriched decision trace blocks."""
from decision_engine_v3.engine.core import DecisionEngineV3
from decision_engine_v3.models.data import ContentMetrics

def _decision():
    e = DecisionEngineV3()
    return e.decide_explore(ContentMetrics(
        views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить","сколько стоит","хочу","беру","ссылку","артикул","нужно","заказать","цена","доставка","заказал","куплю","подарок","дешевле","доставкой"],
        total_comments=15,
    ))

def test_trace_signal_cleaning_has_degraded():
    d = _decision()
    assert "degraded" in d.trace.signal_cleaning
    assert isinstance(d.trace.signal_cleaning["degraded"], bool)

def test_trace_intent_has_penalties():
    d = _decision()
    assert "penalties" in d.trace.intent_engine
    assert "high_hits" in d.trace.intent_engine

def test_trace_evidence_has_gates():
    d = _decision()
    assert "gates_triggered" in d.trace.evidence_engine

def test_trace_antiviral_has_all_scores():
    d = _decision()
    av = d.trace.anti_viral
    assert "curiosity_bait" in av
    assert "rage" in av
    assert "entertainment" in av

def test_trace_economics_has_margin_ok():
    d = _decision()
    assert "margin_ok" in d.trace.economics

def test_trace_policy_has_downgraded():
    d = _decision()
    assert "downgraded" in d.trace.policy_engine
    assert "human_rule" in d.trace.policy_engine

def test_trace_confidence_has_gates():
    d = _decision()
    assert "gates_triggered" in d.trace.confidence_engine
