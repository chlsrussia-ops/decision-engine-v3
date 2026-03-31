"""Domain data models — inputs, intermediate results, engine outputs."""
from __future__ import annotations
from dataclasses import dataclass, field
from .enums import (
    Action, DecisionMode, SaturationState, ReviewMaturity,
    RedFlagSeverity, ReasonCode, CapReasonCode, HumanRuleStatus,
)


@dataclass
class ContentMetrics:
    views: int = 0
    clicks: int = 0
    ctr: float = 0.0
    saves: int = 0
    save_rate: float = 0.0
    comments: list[str] = field(default_factory=list)
    total_comments: int = 0
    likes: int = 0
    shares: int = 0


@dataclass
class MarketplaceMetrics:
    competitors: int = 0
    avg_price: float = 0.0
    min_price: float = 0.0
    max_price: float = 0.0
    avg_reviews: float = 0.0
    avg_rating: float = 0.0
    top_seller_revenue_estimate: float = 0.0
    saturation_state: str = "unknown"
    review_maturity: str = "unknown"


@dataclass
class EconomicsPreview:
    estimated_cost: float = 0.0
    landed_cost: float = 0.0
    target_price: float = 0.0
    estimated_margin_pct: float = 0.0
    market_min_price: float = 0.0
    platform_fee_pct: float = 15.0


@dataclass
class SellMetrics:
    orders: int = 0
    revenue: float = 0.0
    ad_spend: float = 0.0
    roi_pct: float = 0.0
    cvr_pct: float = 0.0
    acos_pct: float = 0.0


@dataclass
class ReviewerContext:
    product_name: str = ""
    category: str = ""
    source: str = ""
    notes: str = ""


# ── Engine results ───────────────────────────────────────────────────

@dataclass
class SignalCleaningResult:
    clean_comments: list[str] = field(default_factory=list)
    clean_comment_count: int = 0
    duplicate_ratio: float = 0.0
    uniqueness_score: float = 1.0
    spam_ratio: float = 0.0
    removed_duplicates: int = 0
    removed_spam: int = 0
    removed_noise: int = 0


@dataclass
class IntentResult:
    raw_intent: float = 0.0
    weighted_intent: float = 0.0
    qualified_intent: float = 0.0
    high_intent_hits: int = 0
    medium_hits: int = 0
    low_hits: int = 0
    skeptical_hits: int = 0
    negative_hits: int = 0
    intent_density: float = 0.0
    strong_intent_share: float = 0.0
    negative_rate: float = 0.0
    top_keywords: list[str] = field(default_factory=list)
    penalties: dict = field(default_factory=dict)


@dataclass
class EvidenceResult:
    comment_confidence: float = 0.0
    volume_confidence: float = 0.0
    click_confidence: float = 0.0
    marketplace_confidence: float = 0.0
    evidence_score: float = 0.0


@dataclass
class AntiViralResult:
    antiviral_score: float = 0.0
    empty_viral_score: float = 0.0
    curiosity_bait_score: float = 0.0
    rage_score: float = 0.0
    entertainment_score: float = 0.0
    misleading_cta_score: float = 0.0
    false_viral_score: float = 0.0
    status: str = "clean"  # clean | caution | discard | hard_block


@dataclass
class ViabilityResult:
    viability: float = 0.0
    components: dict = field(default_factory=dict)
    caps_applied: list[str] = field(default_factory=list)


@dataclass
class ConfidenceResult:
    confidence: float = 0.0
    components: dict = field(default_factory=dict)
    penalties: list[str] = field(default_factory=list)


@dataclass
class MarketplaceModifierResult:
    demand_proof_score: float = 0.0
    pressure_score: float = 0.0
    saturation_state: str = "unknown"
    review_maturity: str = "unknown"
    price_compression: float = 0.0
    price_risk: float = 0.0
    fake_opportunity: float = 0.0
    margin_precheck: str = "unknown"
    viability_adjustment: float = 0.0
    caution_reasons: list[str] = field(default_factory=list)
    block: bool = False


@dataclass
class EconomicsResult:
    estimated_margin_pct: float = 0.0
    margin_ok: bool = True
    landed_above_market_min: bool = False
    status: str = "ok"  # ok | warning | fail


@dataclass
class RedFlag:
    code: str = ""
    severity: str = "info"
    message: str = ""


@dataclass
class DecisionCaps:
    max_allowed_action: Action = Action.SCALE
    reasons: list[CapReasonCode] = field(default_factory=list)


@dataclass
class DecisionTrace:
    signal_cleaning: dict = field(default_factory=dict)
    intent_engine: dict = field(default_factory=dict)
    evidence_engine: dict = field(default_factory=dict)
    anti_viral: dict = field(default_factory=dict)
    marketplace_modifier: dict = field(default_factory=dict)
    economics: dict = field(default_factory=dict)
    viability_engine: dict = field(default_factory=dict)
    confidence_engine: dict = field(default_factory=dict)
    red_flags: list[dict] = field(default_factory=list)
    policy_engine: dict = field(default_factory=dict)


@dataclass
class Decision:
    action: Action = Action.HOLD
    mode: DecisionMode = DecisionMode.EXPLORE
    intent_score: float = 0.0
    viability: float = 0.0
    confidence: float = 0.0
    reasons: list[str] = field(default_factory=list)
    reason_codes: list[ReasonCode] = field(default_factory=list)
    red_flags: list[RedFlag] = field(default_factory=list)
    red_flag_codes: list[str] = field(default_factory=list)
    caps: DecisionCaps = field(default_factory=DecisionCaps)
    trace: DecisionTrace = field(default_factory=DecisionTrace)
    human_rule: HumanRuleStatus = HumanRuleStatus.UNCERTAIN
    degraded: bool = False
    degraded_modules: list[str] = field(default_factory=list)
    fallback_used: bool = False
    module_errors: list[str] = field(default_factory=list)
    engine_version: str = "v3"
