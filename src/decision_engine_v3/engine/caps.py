"""Decision Caps — post-policy action limiting."""
from __future__ import annotations
from ..models.data import DecisionCaps, EvidenceResult, AntiViralResult, ConfidenceResult, EconomicsResult, MarketplaceModifierResult
from ..models.enums import Action, CapReasonCode, HumanRuleStatus


def build_caps(evidence: EvidenceResult, antiviral: AntiViralResult, confidence: ConfidenceResult, economics: EconomicsResult, marketplace: MarketplaceModifierResult | None = None, human_rule: HumanRuleStatus = HumanRuleStatus.UNCERTAIN) -> DecisionCaps:
    caps = DecisionCaps(max_allowed_action=Action.SCALE, reasons=[])

    def cap(action: Action, reason: CapReasonCode):
        if action.severity < caps.max_allowed_action.severity:
            caps.max_allowed_action = action
        caps.reasons.append(reason)

    if evidence.evidence_score < 0.35:
        cap(Action.HOLD, CapReasonCode.EVIDENCE_TOO_LOW)
    if antiviral.antiviral_score >= 0.80:
        cap(Action.DISCARD, CapReasonCode.ANTIVIRAL_HARD_BLOCK)
    elif antiviral.antiviral_score >= 0.60:
        cap(Action.DISCARD, CapReasonCode.ANTIVIRAL_SOFT_BLOCK)
    if confidence.confidence < 0.30:
        cap(Action.HOLD, CapReasonCode.LOW_CONFIDENCE)
    if economics.status == "fail":
        cap(Action.HOLD, CapReasonCode.ECONOMICS_FAIL)
    if marketplace and marketplace.block:
        cap(Action.HOLD, CapReasonCode.MARKETPLACE_BLOCK)
    if human_rule == HumanRuleStatus.SKIP:
        cap(Action.HOLD, CapReasonCode.REVIEWER_STOP_GATE)

    return caps


def apply_cap(policy_action: Action, caps: DecisionCaps) -> Action:
    """Return min(policy_action, cap) by severity ordering."""
    if policy_action.severity > caps.max_allowed_action.severity:
        return caps.max_allowed_action
    return policy_action
