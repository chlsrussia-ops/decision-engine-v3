"""Shadow mode — non-invasive V2 vs V3 comparison. Never mutates primary."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger("decision_engine.shadow")


@dataclass
class ShadowResult:
    v2_action: str = "HOLD"
    v3_action: str = "HOLD"
    action_changed: bool = False
    v2_intent_score: float = 0.0
    v3_qualified_intent: float = 0.0
    v2_viability: float = 0.0
    v3_viability: float = 0.0
    v3_confidence: float = 0.0
    reason_codes: list[str] = field(default_factory=list)
    red_flag_codes: list[str] = field(default_factory=list)
    decision_diff: dict = field(default_factory=dict)
    shadow_error: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def build_shadow_result(v2_action: str, v2_intent: float, v2_viability: float, v3_decision) -> ShadowResult:
    """Build shadow comparison. Safe: never raises, returns error in shadow_error field."""
    try:
        v3_action = v3_decision.action.value
        changed = v2_action != v3_action

        antiviral_status = v3_decision.trace.anti_viral.get("status", "clean") if isinstance(v3_decision.trace.anti_viral, dict) else "unknown"
        evidence_gated = any("evidence" in str(c) for c in v3_decision.caps.reasons) if v3_decision.caps else False

        # Human-readable explanation
        parts = [f"V2={v2_action}, V3={v3_action}"]
        if changed:
            parts.append("ACTION CHANGED")
        if v3_decision.confidence < 0.3:
            parts.append("low confidence")
        if antiviral_status not in ("clean", "unknown"):
            parts.append(f"antiviral={antiviral_status}")
        if evidence_gated:
            parts.append("evidence gate triggered")
        if v3_decision.degraded:
            parts.append(f"degraded modules: {', '.join(v3_decision.degraded_modules)}")

        diff = {
            "intent_delta": round(v3_decision.intent_score - v2_intent, 4),
            "viability_delta": round(v3_decision.viability - v2_viability, 4),
            "confidence_delta": v3_decision.confidence,
            "antiviral_triggered": antiviral_status not in ("clean", "unknown"),
            "evidence_gate_triggered": evidence_gated,
            "v3_degraded": v3_decision.degraded,
            "explanation": " | ".join(parts),
        }

        return ShadowResult(
            v2_action=v2_action, v3_action=v3_action, action_changed=changed,
            v2_intent_score=v2_intent, v3_qualified_intent=v3_decision.intent_score,
            v2_viability=v2_viability, v3_viability=v3_decision.viability,
            v3_confidence=v3_decision.confidence,
            reason_codes=[c.value for c in v3_decision.reason_codes],
            red_flag_codes=v3_decision.red_flag_codes,
            decision_diff=diff,
        )
    except Exception as e:
        logger.error(f"Shadow mode failed: {e}", exc_info=True)
        return ShadowResult(shadow_error=str(e))
