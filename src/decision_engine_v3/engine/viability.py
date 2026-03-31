"""Viability Engine — explainable weighted composite with caps."""
from __future__ import annotations
from ..models.data import ViabilityResult, ContentMetrics, IntentResult, EvidenceResult, AntiViralResult, MarketplaceModifierResult


def compute_viability(content: ContentMetrics, intent: IntentResult, evidence: EvidenceResult, antiviral: AntiViralResult, marketplace: MarketplaceModifierResult | None = None) -> ViabilityResult:
    intent_q = min(intent.qualified_intent / 0.30, 1.0) * 0.30
    save_q = min(content.save_rate / 0.05, 1.0) * 0.25
    ctr_q = min(content.ctr / 0.03, 1.0) * 0.20
    s2c = (content.saves / max(content.clicks, 1)) if content.clicks > 0 else 0.0
    s2c_q = min(s2c / 0.10, 1.0) * 0.10
    market_fit = 0.5 if marketplace and marketplace.demand_proof_score > 0.3 else 0.3
    market_q = market_fit * 0.10
    vol_q = min(evidence.volume_confidence, 1.0) * 0.05

    raw = round(intent_q + save_q + ctr_q + s2c_q + market_q + vol_q, 4)
    caps = []

    if evidence.evidence_score < 0.35:
        raw = min(raw, 0.30); caps.append("weak_evidence_cap")
    if antiviral.false_viral_score >= 0.5:
        raw = min(raw, 0.25); caps.append("false_viral_cap")
    if intent.intent_density < 0.03:
        raw *= 0.85; caps.append("low_intent_density_penalty")
    if intent.negative_rate > 0.2:
        raw *= 0.80; caps.append("high_negative_penalty")
    if marketplace and marketplace.viability_adjustment < 0:
        raw += marketplace.viability_adjustment; caps.append("marketplace_penalty")

    return ViabilityResult(
        viability=round(max(raw, 0.0), 4),
        components={"intent": round(intent_q, 4), "saves": round(save_q, 4), "ctr": round(ctr_q, 4), "s2c": round(s2c_q, 4), "market_fit": round(market_q, 4), "volume": round(vol_q, 4)},
        caps_applied=caps,
    )
