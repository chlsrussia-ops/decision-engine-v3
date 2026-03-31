"""Analytics event and calibration builders — pure, deterministic, zero side effects."""
from datetime import datetime, timezone
from ..models.data import Decision, ContentMetrics, IntentResult, SignalCleaningResult
from ..models.analytics import AnalyticsEvent, CalibrationRow


def build_analytics_event(decision: Decision, content: ContentMetrics | None = None, product_name: str = "", request_id: str = "") -> AnalyticsEvent:
    return AnalyticsEvent(
        event_type="decision_made",
        timestamp=datetime.now(timezone.utc).isoformat(),
        action=decision.action.value,
        mode=decision.mode.value,
        intent_score=decision.intent_score,
        viability=decision.viability,
        confidence=decision.confidence,
        evidence_score=decision.trace.evidence_engine.get("score", 0) if isinstance(decision.trace.evidence_engine, dict) else 0,
        antiviral_score=decision.trace.anti_viral.get("score", 0) if isinstance(decision.trace.anti_viral, dict) else 0,
        degraded=decision.degraded,
        reason_codes=[c.value for c in decision.reason_codes],
        red_flag_codes=decision.red_flag_codes,
        product_name=product_name,
        category="",
    )


def build_calibration_row(decision: Decision, content: ContentMetrics | None = None, intent: IntentResult | None = None, cleaning: SignalCleaningResult | None = None, product_name: str = "") -> CalibrationRow:
    return CalibrationRow(
        action=decision.action.value,
        intent_score=decision.intent_score,
        qualified_intent=intent.qualified_intent if intent else 0.0,
        viability=decision.viability,
        confidence=decision.confidence,
        evidence_score=decision.trace.evidence_engine.get("score", 0.0) if isinstance(decision.trace.evidence_engine, dict) else 0.0,
        antiviral_score=decision.trace.anti_viral.get("score", 0.0) if isinstance(decision.trace.anti_viral, dict) else 0.0,
        views=content.views if content else 0,
        clicks=content.clicks if content else 0,
        ctr=content.ctr if content else 0.0,
        save_rate=content.save_rate if content else 0.0,
        clean_comments=cleaning.clean_comment_count if cleaning else 0,
        negative_rate=intent.negative_rate if intent else 0.0,
        reason_codes=[c.value for c in decision.reason_codes],
        red_flag_codes=decision.red_flag_codes,
        product_name=product_name,
    )
