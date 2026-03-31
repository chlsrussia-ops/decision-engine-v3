"""Explicit response serializer — always returns same keys regardless of flags/degradation."""
from __future__ import annotations
from dataclasses import asdict
from ..models.data import Decision, DecisionTrace


def serialize_decision(d: Decision) -> dict:
    """Stable schema: all keys always present, even if empty/neutral."""
    trace = asdict(d.trace) if d.trace else {}
    return {
        # Legacy V2 (always present)
        "action": d.action.value,
        "intent_score": d.intent_score,
        "viability": d.viability,
        "reasons": d.reasons,
        # V3 extensions (always present, may be neutral)
        "engine_version": d.engine_version,
        "mode": d.mode.value,
        "confidence": d.confidence,
        "reason_codes": [c.value for c in d.reason_codes],
        "red_flags": [{"code": f.code, "severity": f.severity, "message": f.message} for f in d.red_flags],
        "red_flag_codes": d.red_flag_codes,
        "human_rule": d.human_rule.value,
        "caps": {"max_action": d.caps.max_allowed_action.value, "reasons": [c.value for c in d.caps.reasons]},
        "decision_trace": trace,
        # Degradation metadata (always present)
        "degraded": d.degraded,
        "degraded_modules": d.degraded_modules,
        "fallback_used": d.fallback_used,
        "module_errors": d.module_errors,
    }


REQUIRED_KEYS = frozenset([
    "action", "intent_score", "viability", "reasons", "engine_version", "mode",
    "confidence", "reason_codes", "red_flags", "red_flag_codes", "human_rule",
    "caps", "decision_trace", "degraded", "degraded_modules", "fallback_used", "module_errors",
])


def validate_response_schema(response: dict) -> list[str]:
    """Check that response has all required keys."""
    return [k for k in REQUIRED_KEYS if k not in response]
