"""Build ReviewerPacket from Decision + engine results. Works in degraded mode."""
from ..models.data import Decision, ContentMetrics, IntentResult, EvidenceResult, AntiViralResult, ViabilityResult, ConfidenceResult, MarketplaceModifierResult, EconomicsResult
from ..models.reviewer import ReviewerPacket


_FOCUS_SEVERITY = {
    "economics fail": 10,
    "high antiviral": 9,
    "low margin": 8,
    "weak evidence": 7,
    "low confidence": 6,
    "high negative rate": 5,
    "marketplace pressure": 4,
    "low uniqueness": 3,
    "price compression": 2,
    "low views": 1,
}


def build_reviewer_packet(
    decision: Decision,
    content: ContentMetrics | None = None,
    intent: IntentResult | None = None,
    evidence: EvidenceResult | None = None,
    antiviral: AntiViralResult | None = None,
    viability: ViabilityResult | None = None,
    confidence: ConfidenceResult | None = None,
    marketplace: MarketplaceModifierResult | None = None,
    economics: EconomicsResult | None = None,
) -> ReviewerPacket:

    # Review focus — severity ranked
    focus_items: list[tuple[int, str]] = []
    if evidence and evidence.evidence_score < 0.4:
        focus_items.append((_FOCUS_SEVERITY["weak evidence"], "weak evidence"))
    if antiviral and antiviral.antiviral_score >= 0.4:
        focus_items.append((_FOCUS_SEVERITY["high antiviral"], "high antiviral"))
    if confidence and confidence.confidence < 0.35:
        focus_items.append((_FOCUS_SEVERITY["low confidence"], "low confidence"))
    if intent and intent.negative_rate > 0.15:
        focus_items.append((_FOCUS_SEVERITY["high negative rate"], "high negative rate"))
    if economics and economics.status == "fail":
        focus_items.append((_FOCUS_SEVERITY["economics fail"], "economics fail"))
    if marketplace and marketplace.pressure_score > 0.6:
        focus_items.append((_FOCUS_SEVERITY["marketplace pressure"], "marketplace pressure"))
    if marketplace and marketplace.price_compression > 0.7:
        focus_items.append((_FOCUS_SEVERITY["price compression"], "price compression"))
    if content and content.views < 1000:
        focus_items.append((_FOCUS_SEVERITY["low views"], "low views"))

    focus_items.sort(key=lambda x: x[0], reverse=True)
    review_focus = [item[1] for item in focus_items]

    # Checklist — always useful
    checklist = ["Verify intent quality manually", "Check product-market fit", "Review red flags"]
    if decision.action.value in ("TEST_PRODUCT", "CAUTION"):
        checklist.append("Confirm willingness to invest test budget")
    if decision.degraded:
        checklist.append(f"⚠️ DEGRADED: modules failed = {', '.join(decision.degraded_modules)}")
        checklist.append("Review module_errors before approving")

    # Confidence explanation — from real data only
    if confidence and confidence.confidence > 0:
        penalties_str = f", penalties: {', '.join(confidence.penalties)}" if confidence.penalties else ""
        conf_text = f"Confidence {confidence.confidence:.2f} based on comment={confidence.components.get('comment', 0):.2f}, volume={confidence.components.get('volume', 0):.2f}{penalties_str}"
    elif decision.degraded and "confidence" in decision.degraded_modules:
        conf_text = "Confidence unavailable — module failed"
    else:
        conf_text = f"Confidence {decision.confidence:.2f} (engine-level, no detailed breakdown available)"

    # Viability summary — only real data
    via_summary: dict = {}
    if viability:
        via_summary = {"score": viability.viability, "components": viability.components, "caps": viability.caps_applied}
    else:
        via_summary = {"score": decision.viability, "components": {}, "caps": [], "note": "detailed breakdown unavailable"}

    # Marketplace summary — safe for partial failure
    mkt_summary: dict = {}
    if marketplace:
        mkt_summary = {"saturation": marketplace.saturation_state, "pressure": marketplace.pressure_score, "demand_proof": marketplace.demand_proof_score, "caution_reasons": marketplace.caution_reasons}
    else:
        mkt_summary = {"saturation": "unknown", "pressure": 0, "note": "marketplace data unavailable"}

    return ReviewerPacket(
        recommendation=decision.action.value,
        confidence=decision.confidence,
        confidence_explanation=conf_text,
        key_metrics={
            "views": content.views if content else 0,
            "clicks": content.clicks if content else 0,
            "ctr": content.ctr if content else 0,
            "save_rate": content.save_rate if content else 0,
            "saves": content.saves if content else 0,
        },
        intent_summary={
            "qualified_intent": intent.qualified_intent if intent else 0,
            "raw_intent": intent.raw_intent if intent else 0,
            "density": intent.intent_density if intent else 0,
            "negative_rate": intent.negative_rate if intent else 0,
            "strong_intent_share": intent.strong_intent_share if intent else 0,
            "top_keywords": intent.top_keywords[:5] if intent else [],
        },
        viability_summary=via_summary,
        evidence_score=evidence.evidence_score if evidence else 0,
        antiviral_score=antiviral.antiviral_score if antiviral else 0,
        marketplace_summary=mkt_summary,
        economics_summary={"margin": economics.estimated_margin_pct if economics else 0, "status": economics.status if economics else "unknown", "landed_above_market": economics.landed_above_market_min if economics else False},
        red_flags=[{"code": f.code, "severity": f.severity, "message": f.message} for f in decision.red_flags],
        top_reasons=decision.reasons[:5],
        review_focus=review_focus,
        reviewer_checklist=checklist,
        human_rule=decision.human_rule.value,
    )
