"""Evidence Sufficiency Engine — how much can we trust the signal."""
from __future__ import annotations
from ..models.data import EvidenceResult, ContentMetrics, MarketplaceMetrics, SignalCleaningResult


def compute_evidence(content: ContentMetrics, marketplace: MarketplaceMetrics | None = None, cleaning: SignalCleaningResult | None = None) -> EvidenceResult:
    clean_count = cleaning.clean_comment_count if cleaning else content.total_comments
    comment_conf = min(clean_count / 30.0, 1.0)
    volume_conf = min(content.views / 3000.0, 1.0)
    click_conf = min(content.clicks / 50.0, 1.0)
    market_conf = 0.3
    if marketplace and marketplace.competitors > 0:
        market_conf = min(0.3 + marketplace.competitors / 50.0, 1.0)

    evidence = round(
        comment_conf * 0.35 + volume_conf * 0.30 + click_conf * 0.20 + market_conf * 0.15, 4
    )
    return EvidenceResult(
        comment_confidence=round(comment_conf, 4),
        volume_confidence=round(volume_conf, 4),
        click_confidence=round(click_conf, 4),
        marketplace_confidence=round(market_conf, 4),
        evidence_score=evidence,
    )
