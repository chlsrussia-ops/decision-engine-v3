from decision_engine_v3.engine.reasoning import build_red_flags, build_readable_summary
from decision_engine_v3.models.data import ContentMetrics, IntentResult, EvidenceResult, AntiViralResult, ConfidenceResult, EconomicsResult, MarketplaceModifierResult, ViabilityResult, RedFlag

def test_red_flags_low_save():
    flags = build_red_flags(ContentMetrics(save_rate=0.005, ctr=0.005, views=500, clicks=10), IntentResult(), EvidenceResult(evidence_score=0.3), AntiViralResult(), ConfidenceResult(confidence=0.3), EconomicsResult(), MarketplaceModifierResult(), ViabilityResult())
    codes = [f.code for f in flags]
    assert "weak_save_rate" in codes
    assert "weak_evidence" in codes

def test_red_flags_economics_fail():
    flags = build_red_flags(ContentMetrics(save_rate=0.03, ctr=0.02, views=3000, clicks=60), IntentResult(), EvidenceResult(evidence_score=0.6), AntiViralResult(), ConfidenceResult(confidence=0.5), EconomicsResult(status="fail", estimated_margin_pct=5.0), MarketplaceModifierResult(), ViabilityResult())
    codes = [f.code for f in flags]
    assert "economics_fail" in codes

def test_readable_summary():
    s = build_readable_summary("HOLD", ["low views"], [RedFlag("weak_evidence", "hard", "ev=0.2")], False)
    assert "HOLD" in s
    assert "weak_evidence" in s

def test_summary_degraded():
    s = build_readable_summary("HOLD", [], [], True)
    assert "Degraded" in s
