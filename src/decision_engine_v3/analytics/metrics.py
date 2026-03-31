"""Monitoring metrics patterns — structured log helpers."""
from ..models.data import Decision


def decision_log_payload(d: Decision, product_name: str = "") -> dict:
    """Structured log payload for every decision."""
    return {
        "event": "decision_engine.decision",
        "action": d.action.value,
        "mode": d.mode.value,
        "intent_score": d.intent_score,
        "viability": d.viability,
        "confidence": d.confidence,
        "degraded": d.degraded,
        "degraded_modules": d.degraded_modules,
        "reason_codes": [c.value for c in d.reason_codes],
        "red_flag_count": len(d.red_flags),
        "hard_flag_count": sum(1 for f in d.red_flags if f.severity == "hard"),
        "human_rule": d.human_rule.value,
        "cap_reasons": [c.value for c in d.caps.reasons],
        "product_name": product_name,
    }
