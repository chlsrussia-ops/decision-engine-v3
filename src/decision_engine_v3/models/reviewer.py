"""Reviewer packet model."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ReviewerPacket:
    recommendation: str = "HOLD"
    confidence: float = 0.0
    confidence_explanation: str = ""
    key_metrics: dict = field(default_factory=dict)
    intent_summary: dict = field(default_factory=dict)
    viability_summary: dict = field(default_factory=dict)
    evidence_score: float = 0.0
    antiviral_score: float = 0.0
    marketplace_summary: dict = field(default_factory=dict)
    economics_summary: dict = field(default_factory=dict)
    red_flags: list[dict] = field(default_factory=list)
    top_reasons: list[str] = field(default_factory=list)
    review_focus: list[str] = field(default_factory=list)
    reviewer_checklist: list[str] = field(default_factory=list)
    human_rule: str = "uncertain"
