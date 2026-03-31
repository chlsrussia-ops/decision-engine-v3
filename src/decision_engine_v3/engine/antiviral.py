"""Anti-Viral Engine V3 — detect empty viral, curiosity bait, rage, entertainment."""
from __future__ import annotations
from ..models.data import AntiViralResult, ContentMetrics, IntentResult


def compute_antiviral(content: ContentMetrics, intent: IntentResult) -> AntiViralResult:
    v, ctr, sr = content.views, content.ctr, content.save_rate

    empty_viral = 0.0
    if v >= 1500 and ctr < 0.005 and sr < 0.02 and intent.qualified_intent < 0.05:
        empty_viral = min(0.3 + (1500 / max(v, 1)) * 0.1 + (0.02 - sr) * 5, 1.0)

    curiosity = 0.0
    if v >= 1000 and intent.intent_density < 0.05 and sr < 0.015:
        curiosity = min(0.4 + (0.05 - intent.intent_density) * 5, 1.0)

    rage = 0.0
    if intent.negative_rate > 0.3:
        rage = min(intent.negative_rate * 1.5, 1.0)

    entertainment = 0.0
    if v >= 2000 and content.likes > content.saves * 10 and intent.intent_density < 0.03:
        entertainment = min(0.5 + (content.likes / max(content.saves, 1)) * 0.01, 1.0)

    misleading = 0.0
    if ctr > 0.05 and sr < 0.01 and intent.qualified_intent < 0.03:
        misleading = min(0.5 + (ctr - 0.05) * 5, 1.0)

    false_viral = max(empty_viral, curiosity, rage, entertainment, misleading)
    aggregate = round(
        empty_viral * 0.25 + curiosity * 0.20 + rage * 0.20 +
        entertainment * 0.15 + misleading * 0.10 + false_viral * 0.10, 4
    )

    if aggregate >= 0.80: status = "hard_block"
    elif aggregate >= 0.60: status = "discard"
    elif aggregate >= 0.40: status = "caution"
    else: status = "clean"

    return AntiViralResult(
        antiviral_score=aggregate, empty_viral_score=round(empty_viral, 4),
        curiosity_bait_score=round(curiosity, 4), rage_score=round(rage, 4),
        entertainment_score=round(entertainment, 4), misleading_cta_score=round(misleading, 4),
        false_viral_score=round(false_viral, 4), status=status,
    )
