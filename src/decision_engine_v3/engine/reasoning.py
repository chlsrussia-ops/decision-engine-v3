"""Reason code builders, red flag builders, readable summaries."""
from ..models.data import RedFlag, ContentMetrics, IntentResult, EvidenceResult, AntiViralResult, ConfidenceResult, EconomicsResult, MarketplaceModifierResult, ViabilityResult


def build_red_flags(content: ContentMetrics, intent: IntentResult, evidence: EvidenceResult, antiviral: AntiViralResult, confidence: ConfidenceResult, economics: EconomicsResult, marketplace: MarketplaceModifierResult, viability: ViabilityResult) -> list[RedFlag]:
    flags = []
    if content.save_rate < 0.015:
        flags.append(RedFlag("weak_save_rate", "moderate", f"save_rate={content.save_rate:.3f}"))
    if content.ctr < 0.008:
        flags.append(RedFlag("weak_ctr", "moderate", f"ctr={content.ctr:.3f}"))
    if content.views < 1000:
        flags.append(RedFlag("low_views", "info", f"views={content.views}"))
    if content.clicks < 20:
        flags.append(RedFlag("low_clicks", "info", f"clicks={content.clicks}"))
    if antiviral.antiviral_score >= 0.4:
        sev = "hard" if antiviral.antiviral_score >= 0.6 else "moderate"
        flags.append(RedFlag("antiviral_warning", sev, f"antiviral={antiviral.antiviral_score:.3f}"))
    if antiviral.false_viral_score >= 0.5:
        flags.append(RedFlag("false_viral", "hard", f"false_viral={antiviral.false_viral_score:.3f}"))
    if intent.negative_rate > 0.15:
        flags.append(RedFlag("high_negative_rate", "moderate", f"neg_rate={intent.negative_rate:.3f}"))
    if intent.intent_density < 0.05 and content.views >= 1000:
        flags.append(RedFlag("low_intent_density", "moderate", f"density={intent.intent_density:.3f}"))
    if evidence.evidence_score < 0.4:
        flags.append(RedFlag("weak_evidence", "moderate", f"evidence={evidence.evidence_score:.3f}"))
    if confidence.confidence < 0.35:
        flags.append(RedFlag("low_confidence", "moderate", f"confidence={confidence.confidence:.3f}"))
    if economics.status == "fail":
        flags.append(RedFlag("economics_fail", "hard", f"margin={economics.estimated_margin_pct:.1f}%"))
    if economics.landed_above_market_min:
        flags.append(RedFlag("cost_above_market", "hard", "landed_cost > market_min"))
    if marketplace.pressure_score > 0.6:
        flags.append(RedFlag("high_pressure", "moderate", f"pressure={marketplace.pressure_score:.3f}"))
    if marketplace.saturation_state == "dead":
        flags.append(RedFlag("dead_market", "hard", "saturation=dead"))
    if marketplace.saturation_state == "virgin":
        flags.append(RedFlag("virgin_market", "info", "saturation=virgin, unproven demand"))
    if marketplace.fake_opportunity >= 0.5:
        flags.append(RedFlag("fake_opportunity", "hard", f"fake_opp={marketplace.fake_opportunity:.3f}"))
    return flags


def build_readable_summary(action: str, reasons: list[str], red_flags: list[RedFlag], degraded: bool) -> str:
    parts = [f"Action: {action}"]
    if reasons:
        parts.append(f"Reasons: {'; '.join(reasons[:3])}")
    hard = [f.code for f in red_flags if f.severity == "hard"]
    if hard:
        parts.append(f"Hard flags: {', '.join(hard)}")
    if degraded:
        parts.append("⚠️ Degraded execution")
    return " | ".join(parts)
