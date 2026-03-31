"""Confidence Engine — separate from viability. How much we trust the signal."""
from __future__ import annotations
from ..models.data import ConfidenceResult, EvidenceResult, SignalCleaningResult, MarketplaceModifierResult


def compute_confidence(evidence: EvidenceResult, cleaning: SignalCleaningResult | None = None, marketplace: MarketplaceModifierResult | None = None) -> ConfidenceResult:
    comment_c = evidence.comment_confidence * 0.35
    volume_c = evidence.volume_confidence * 0.25
    market_c = (marketplace.demand_proof_score if marketplace else 0.3) * 0.20
    consistency = 0.5  # baseline
    if cleaning and cleaning.uniqueness_score > 0.7:
        consistency = 0.7
    if cleaning and cleaning.uniqueness_score > 0.9:
        consistency = 0.9
    consistency_c = consistency * 0.20

    raw = round(comment_c + volume_c + market_c + consistency_c, 4)
    penalties = []
    if evidence.evidence_score < 0.35:
        raw = min(raw, 0.40); penalties.append("low_evidence_cap")
    if cleaning and cleaning.uniqueness_score < 0.5:
        raw *= 0.85; penalties.append("low_uniqueness")
    if cleaning and cleaning.clean_comment_count < 10:
        raw *= 0.90; penalties.append("small_sample")

    return ConfidenceResult(
        confidence=round(max(raw, 0.0), 4),
        components={"comment": round(comment_c, 4), "volume": round(volume_c, 4), "marketplace": round(market_c, 4), "consistency": round(consistency_c, 4)},
        penalties=penalties,
    )
