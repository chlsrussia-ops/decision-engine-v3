"""Integration wrapper — main entry point for external callers."""
from __future__ import annotations
from ..models.requests import LegacyExplorePayload, LegacySellPayload
from ..flags.config import FeatureFlags
from ..engine.core import DecisionEngineV3
from ..adapters.legacy_input import map_explore_input, map_sell_input
from ..adapters.validation import validate_explore_payload, validate_sell_payload, PayloadValidationError
from ..wrapper.serializer import serialize_decision
from ..wrapper.reviewer_packet import build_reviewer_packet
from ..wrapper.shadow import build_shadow_result
from ..analytics.metrics import decision_log_payload
from dataclasses import asdict
import logging

logger = logging.getLogger("decision_engine.wrapper")


class DecisionEngineWrapper:
    def __init__(self, flags: FeatureFlags | None = None):
        self.flags = flags or FeatureFlags()
        self.flags.validate_strict()
        self.engine = DecisionEngineV3(self.flags)

    def evaluate_explore(self, payload: LegacyExplorePayload, v2_action: str | None = None, v2_intent: float = 0.0, v2_viability: float = 0.0) -> dict:
        errors = validate_explore_payload(payload)
        if errors:
            logger.warning(f"Payload validation warnings: {errors}")

        content, marketplace, economics, reviewer = map_explore_input(payload)
        decision = self.engine.decide_explore(content, marketplace, economics, reviewer)
        response = serialize_decision(decision)

        # Structured log
        logger.info("decision", extra=decision_log_payload(decision, payload.product_name))

        if self.flags.enable_reviewer_packet:
            packet = build_reviewer_packet(decision, content=content)
            response["reviewer_packet"] = asdict(packet)

        if self.flags.enable_shadow_mode and v2_action:
            shadow = build_shadow_result(v2_action, v2_intent, v2_viability, decision)
            response["shadow"] = shadow.to_dict()

        return response

    def evaluate_sell(self, payload: LegacySellPayload) -> dict:
        errors = validate_sell_payload(payload)
        if errors:
            logger.warning(f"Sell payload validation warnings: {errors}")

        sell = map_sell_input(payload)
        decision = self.engine.decide_sell(sell)
        response = serialize_decision(decision)
        logger.info("decision", extra=decision_log_payload(decision, payload.product_name))
        return response
