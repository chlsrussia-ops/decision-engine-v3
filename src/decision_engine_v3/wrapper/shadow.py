"""Shadow mode — compare V2 vs V3 decisions."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict


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

    def to_dict(self) -> dict:
        return asdict(self)


def build_shadow_result(v2_action: str, v2_intent: float, v2_viability: float, v3_decision) -> ShadowResult:
    """Build shadow comparison. v3_decision is a Decision dataclass."""
    v3_action = v3_decision.action.value
    changed = v2_action != v3_action

    diff = {
        "intent_delta": round(v3_decision.intent_score - v2_intent, 4),
        "viability_delta": round(v3_decision.viability - v2_viability, 4),
        "confidence_delta": v3_decision.confidence,
        "antiviral_triggered": v3_decision.trace.anti_viral.get("status", "clean") != "clean",
        "evidence_gate_triggered": any("evidence" in str(c) for c in v3_decision.caps.reasons),
        "explanation": f"V2={v2_action} V3={v3_action}. {'Action changed.' if changed else 'Same action.'} V3 confidence={v3_decision.confidence:.2f}",
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
