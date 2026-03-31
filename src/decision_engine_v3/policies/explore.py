"""Explore policy — hard gates, positive paths, caution basis."""
from __future__ import annotations
from ..models.enums import Action, ReasonCode
from ..models.data import ContentMetrics, IntentResult, EvidenceResult, ViabilityResult
from ..flags.config import FeatureFlags


def decide_explore_action(content: ContentMetrics, intent: IntentResult, evidence: EvidenceResult, viability: ViabilityResult, flags: FeatureFlags) -> tuple[Action, list[str], list[ReasonCode]]:
    reasons = []
    codes: list[ReasonCode] = []
    qi = intent.qualified_intent if flags.enable_qualified_intent else intent.raw_intent

    # Hard gates
    if content.save_rate < 0.01:
        return Action.NEVER_TEST, ["save_rate < 1%"], [ReasonCode.LOW_SAVE_RATE]
    clean_count = content.total_comments
    if clean_count < 5:
        return Action.HOLD, ["comments < 5"], [ReasonCode.LOW_COMMENTS]

    # Soft gates
    if content.views < 500:
        reasons.append("views < 500"); codes.append(ReasonCode.LOW_VIEWS)
        return Action.HOLD, reasons, codes
    if content.ctr < 0.005:
        reasons.append("ctr < 0.5%"); codes.append(ReasonCode.LOW_CTR)
        return Action.HOLD, reasons, codes

    # Positive paths
    if qi >= 0.15 and content.ctr >= 0.005:
        reasons.append(f"intent={qi:.3f}>=0.15 + ctr={content.ctr:.3f}>=0.5%")
        codes.append(ReasonCode.GOOD_INTENT_CTR)
        return Action.TEST_PRODUCT, reasons, codes
    if content.save_rate >= 0.02 and content.clicks >= 15:
        reasons.append(f"save_rate={content.save_rate:.3f}>=2% + clicks={content.clicks}>=15")
        codes.append(ReasonCode.GOOD_SAVE_CLICKS)
        return Action.TEST_PRODUCT, reasons, codes
    if viability.viability >= 0.4 and qi >= 0.15:
        reasons.append(f"viability={viability.viability:.3f}>=0.4 + intent={qi:.3f}>=0.15")
        codes.append(ReasonCode.GOOD_VIABILITY_INTENT)
        return Action.TEST_PRODUCT, reasons, codes

    reasons.append("no positive path matched")
    return Action.HOLD, reasons, codes
