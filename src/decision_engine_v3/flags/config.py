"""Feature flags with dependency validation."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class FeatureFlags:
    enable_signal_cleaning: bool = True
    enable_qualified_intent: bool = True
    enable_antiviral_v3: bool = True
    enable_marketplace_modifier_v3: bool = True
    enable_confidence_engine: bool = True
    enable_caution_status: bool = True
    enable_decision_trace: bool = True
    enable_reviewer_packet: bool = True
    enable_shadow_mode: bool = False

    def validate(self) -> list[str]:
        errors = []
        if self.enable_qualified_intent and not self.enable_signal_cleaning:
            errors.append("qualified_intent requires signal_cleaning")
        if self.enable_shadow_mode and not self.enable_decision_trace:
            errors.append("shadow_mode requires decision_trace")
        return errors

    def validate_strict(self):
        errors = self.validate()
        if errors:
            raise ValueError(f"Invalid flag combination: {errors}")
