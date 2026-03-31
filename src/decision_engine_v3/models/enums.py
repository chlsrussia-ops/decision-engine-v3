"""Canonical enums for Decision Engine V3."""
from enum import Enum


class Action(str, Enum):
    SCALE = "SCALE"
    TEST_PRODUCT = "TEST_PRODUCT"
    CAUTION = "CAUTION"
    HOLD = "HOLD"
    PAUSE = "PAUSE"
    DISCARD = "DISCARD"
    NEVER_TEST = "NEVER_TEST"

    @property
    def severity(self) -> int:
        return _ACTION_SEVERITY[self]


_ACTION_SEVERITY = {
    Action.NEVER_TEST: 0,
    Action.DISCARD: 1,
    Action.PAUSE: 2,
    Action.HOLD: 3,
    Action.CAUTION: 4,
    Action.TEST_PRODUCT: 5,
    Action.SCALE: 6,
}


class DecisionMode(str, Enum):
    EXPLORE = "explore"
    SELL = "sell"


class SaturationState(str, Enum):
    VIRGIN = "virgin"
    EMERGING = "emerging"
    GROWING = "growing"
    MATURE = "mature"
    SATURATED = "saturated"
    DEAD = "dead"


class ReviewMaturity(str, Enum):
    NO_REVIEWS = "no_reviews"
    FEW = "few"
    MODERATE = "moderate"
    ESTABLISHED = "established"
    MATURE = "mature"


class RedFlagSeverity(str, Enum):
    HARD = "hard"
    MODERATE = "moderate"
    INFO = "info"


class ReasonCode(str, Enum):
    LOW_SAVE_RATE = "low_save_rate"
    LOW_COMMENTS = "low_comments"
    LOW_VIEWS = "low_views"
    LOW_CTR = "low_ctr"
    LOW_CLICKS = "low_clicks"
    LOW_EVIDENCE = "low_evidence"
    LOW_CONFIDENCE = "low_confidence"
    LOW_INTENT = "low_intent"
    LOW_MARGIN = "low_margin"
    HIGH_ANTIVIRAL = "high_antiviral"
    HIGH_NEGATIVE = "high_negative"
    HIGH_SPAM = "high_spam"
    HIGH_PRESSURE = "high_pressure"
    DEAD_SATURATION = "dead_saturation"
    GOOD_INTENT_CTR = "good_intent_ctr"
    GOOD_SAVE_CLICKS = "good_save_clicks"
    GOOD_VIABILITY_INTENT = "good_viability_intent"
    SELL_LOW_ORDERS = "sell_low_orders"
    SELL_LOW_ROI = "sell_low_roi"
    SELL_GOOD_ROI_CVR = "sell_good_roi_cvr"
    REVIEWER_BLOCK = "reviewer_block"
    ECONOMICS_FAIL = "economics_fail"
    ANTIVIRAL_BLOCK = "antiviral_block"
    EVIDENCE_CAP = "evidence_cap"
    CONFIDENCE_CAP = "confidence_cap"
    MARKETPLACE_BLOCK = "marketplace_block"


class CapReasonCode(str, Enum):
    EVIDENCE_TOO_LOW = "evidence_too_low"
    ANTIVIRAL_HARD_BLOCK = "antiviral_hard_block"
    ANTIVIRAL_SOFT_BLOCK = "antiviral_soft_block"
    HIGH_NEGATIVE_RATE = "high_negative_rate"
    LOW_CONFIDENCE = "low_confidence"
    REVIEWER_STOP_GATE = "reviewer_stop_gate"
    ECONOMICS_FAIL = "economics_fail"
    MARKETPLACE_BLOCK = "marketplace_block"


class HumanRuleStatus(str, Enum):
    INVEST = "would_invest"
    SKIP = "would_skip"
    UNCERTAIN = "uncertain"
