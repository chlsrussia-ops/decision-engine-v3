"""Build ReviewerPacket from Decision + inputs."""
from ..models.data import Decision, ContentMetrics, IntentResult, EvidenceResult, AntiViralResult, ViabilityResult, ConfidenceResult, MarketplaceModifierResult, EconomicsResult
from ..models.reviewer import ReviewerPacket


def build_reviewer_packet(decision: Decision, content: ContentMetrics | None = None, intent: IntentResult | None = None, evidence: EvidenceResult | None = None, antiviral: AntiViralResult | None = None, viability: ViabilityResult | None = None, confidence: ConfidenceResult | None = None, marketplace: MarketplaceModifierResult | None = None, economics: EconomicsResult | None = None) -> ReviewerPacket:
    review_focus = []
    if evidence and evidence.evidence_score < 0.4: review_focus.append("weak evidence")
    if antiviral and antiviral.antiviral_score >= 0.4: review_focus.append("high antiviral")
    if confidence and confidence.confidence < 0.35: review_focus.append("low confidence")
    if intent and intent.negative_rate > 0.15: review_focus.append("high negative rate")
    if economics and economics.status == "fail": review_focus.append("economics concern")
    if marketplace and marketplace.pressure_score > 0.6: review_focus.append("marketplace pressure")

    checklist = ["Verify intent quality manually", "Check product-market fit", "Review red flags"]
    if decision.action.value in ("TEST_PRODUCT", "CAUTION"):
        checklist.append("Confirm willingness to invest test budget")
    if decision.degraded:
        checklist.append("⚠️ Some modules failed — review degraded_modules")

    conf_explanation = "high" if decision.confidence >= 0.6 else "moderate" if decision.confidence >= 0.35 else "low"

    return ReviewerPacket(
        recommendation=decision.action.value,
        confidence=decision.confidence,
        confidence_explanation=f"Signal confidence is {conf_explanation} ({decision.confidence:.2f})",
        key_metrics={"views": content.views if content else 0, "clicks": content.clicks if content else 0, "ctr": content.ctr if content else 0, "save_rate": content.save_rate if content else 0},
        intent_summary={"qualified_intent": intent.qualified_intent if intent else 0, "density": intent.intent_density if intent else 0, "negative_rate": intent.negative_rate if intent else 0},
        viability_summary={"score": viability.viability if viability else 0, "caps": viability.caps_applied if viability else []},
        evidence_score=evidence.evidence_score if evidence else 0,
        antiviral_score=antiviral.antiviral_score if antiviral else 0,
        marketplace_summary={"saturation": marketplace.saturation_state if marketplace else "unknown", "pressure": marketplace.pressure_score if marketplace else 0},
        economics_summary={"margin": economics.estimated_margin_pct if economics else 0, "status": economics.status if economics else "unknown"},
        red_flags=[{"code": f.code, "severity": f.severity, "message": f.message} for f in decision.red_flags],
        top_reasons=decision.reasons[:5],
        review_focus=review_focus,
        reviewer_checklist=checklist,
        human_rule=decision.human_rule.value,
    )
