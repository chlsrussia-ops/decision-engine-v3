from decision_engine_v3.policies.reviewer_rules import evaluate_human_rule
from decision_engine_v3.models.data import IntentResult, EvidenceResult, ConfidenceResult, ViabilityResult, AntiViralResult
from decision_engine_v3.models.enums import HumanRuleStatus

def test_skip_on_high_antiviral():
    r = evaluate_human_rule(IntentResult(), EvidenceResult(evidence_score=0.5), ConfidenceResult(confidence=0.5), ViabilityResult(viability=0.5), AntiViralResult(antiviral_score=0.7))
    assert r == HumanRuleStatus.SKIP

def test_invest_on_strong_signal():
    r = evaluate_human_rule(IntentResult(qualified_intent=0.2), EvidenceResult(evidence_score=0.6), ConfidenceResult(confidence=0.5), ViabilityResult(viability=0.5), AntiViralResult(antiviral_score=0.1))
    assert r == HumanRuleStatus.INVEST

def test_skip_on_low_evidence():
    r = evaluate_human_rule(IntentResult(qualified_intent=0.2), EvidenceResult(evidence_score=0.2), ConfidenceResult(confidence=0.5), ViabilityResult(viability=0.5), AntiViralResult())
    assert r == HumanRuleStatus.SKIP
