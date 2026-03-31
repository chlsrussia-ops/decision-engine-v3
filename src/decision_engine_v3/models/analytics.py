"""Analytics event and calibration models."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AnalyticsEvent:
    event_type: str = "decision_made"
    timestamp: str = ""
    action: str = "HOLD"
    mode: str = "explore"
    intent_score: float = 0.0
    viability: float = 0.0
    confidence: float = 0.0
    evidence_score: float = 0.0
    antiviral_score: float = 0.0
    degraded: bool = False
    reason_codes: list[str] = field(default_factory=list)
    red_flag_codes: list[str] = field(default_factory=list)
    product_name: str = ""
    category: str = ""


@dataclass
class CalibrationRow:
    action: str = "HOLD"
    intent_score: float = 0.0
    qualified_intent: float = 0.0
    viability: float = 0.0
    confidence: float = 0.0
    evidence_score: float = 0.0
    antiviral_score: float = 0.0
    views: int = 0
    clicks: int = 0
    ctr: float = 0.0
    save_rate: float = 0.0
    clean_comments: int = 0
    negative_rate: float = 0.0
    reason_codes: list[str] = field(default_factory=list)
    red_flag_codes: list[str] = field(default_factory=list)
    product_name: str = ""
