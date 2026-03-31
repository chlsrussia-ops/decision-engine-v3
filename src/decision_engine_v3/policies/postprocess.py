"""Red flags collection."""
from __future__ import annotations
from ..models.data import RedFlag, ContentMetrics, IntentResult, EvidenceResult, AntiViralResult, ConfidenceResult, EconomicsResult, MarketplaceModifierResult, ViabilityResult


def collect_red_flags(content: ContentMetrics, intent: IntentResult, evidence: EvidenceResult, antiviral: AntiViralResult, confidence: ConfidenceResult, economics: EconomicsResult, marketplace: MarketplaceModifierResult, viability: ViabilityResult) -> list[RedFlag]:
    flags = []
    if content.save_rate < 0.015:
        flags.append(RedFlag("weak_save_rate", "moderate", f"save_rate={content.save_rate:.3f}"))
    if content.ctr < 0.008:
        flags.append(RedFlag("weak_ctr", "moderate", f"ctr={content.ctr:.3f}"))
    if content.views < 1000:
        flags.append(RedFlag("low_views", "info", f"views={content.views}"))
    if antiviral.antiviral_score >= 0.4:
        flags.append(RedFlag("antiviral_warning", "hard" if antiviral.antiviral_score >= 0.6 else "moderate", f"antiviral={antiviral.antiviral_score:.3f}"))
    if intent.negative_rate > 0.15:
        flags.append(RedFlag("high_negative_rate", "moderate", f"neg_rate={intent.negative_rate:.3f}"))
    if evidence.evidence_score < 0.4:
        flags.append(RedFlag("weak_evidence", "moderate", f"evidence={evidence.evidence_score:.3f}"))
    if confidence.confidence < 0.35:
        flags.append(RedFlag("low_confidence", "moderate", f"confidence={confidence.confidence:.3f}"))
    if economics.status == "fail":
        flags.append(RedFlag("economics_fail", "hard", f"margin={economics.estimated_margin_pct:.1f}%"))
    if marketplace.pressure_score > 0.6:
        flags.append(RedFlag("high_pressure", "moderate", f"pressure={marketplace.pressure_score:.3f}"))
    if marketplace.saturation_state == "dead":
        flags.append(RedFlag("dead_market", "hard", "saturation=dead"))
    return flags
