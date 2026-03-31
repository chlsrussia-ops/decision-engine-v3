"""Response contracts — backward-compatible + extended."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from .data import Decision, DecisionTrace, RedFlag
from .enums import Action


def decision_to_legacy_response(d: Decision) -> dict:
    """Backward-compatible V2 response + V3 extensions."""
    return {
        # Legacy V2 fields
        "action": d.action.value,
        "intent_score": d.intent_score,
        "viability": d.viability,
        "reasons": d.reasons,
        # V3 extensions
        "engine_version": d.engine_version,
        "confidence": d.confidence,
        "reason_codes": [c.value for c in d.reason_codes],
        "red_flags": [{"code": f.code, "severity": f.severity, "message": f.message} for f in d.red_flags],
        "red_flag_codes": d.red_flag_codes,
        "human_rule": d.human_rule.value,
        "decision_trace": asdict(d.trace),
        # Degradation metadata
        "degraded": d.degraded,
        "degraded_modules": d.degraded_modules,
        "fallback_used": d.fallback_used,
        "module_errors": d.module_errors,
    }
