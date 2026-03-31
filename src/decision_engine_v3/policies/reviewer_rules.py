"""Reviewer human stop-gate."""
from __future__ import annotations
from ..models.enums import HumanRuleStatus
from ..models.data import IntentResult, EvidenceResult, ConfidenceResult, ViabilityResult, AntiViralResult


def evaluate_human_rule(intent: IntentResult, evidence: EvidenceResult, confidence: ConfidenceResult, viability: ViabilityResult, antiviral: AntiViralResult) -> HumanRuleStatus:
    if antiviral.antiviral_score >= 0.6:
        return HumanRuleStatus.SKIP
    if evidence.evidence_score < 0.3:
        return HumanRuleStatus.SKIP
    if confidence.confidence < 0.25:
        return HumanRuleStatus.SKIP
    if viability.viability >= 0.35 and intent.qualified_intent >= 0.10 and confidence.confidence >= 0.35:
        return HumanRuleStatus.INVEST
    return HumanRuleStatus.UNCERTAIN
