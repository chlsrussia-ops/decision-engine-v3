"""Sell policy — HOLD/PAUSE/SCALE."""
from __future__ import annotations
from ..models.enums import Action, ReasonCode
from ..models.data import SellMetrics


def decide_sell_action(sell: SellMetrics) -> tuple[Action, list[str], list[ReasonCode]]:
    if sell.orders < 5:
        return Action.HOLD, ["orders < 5"], [ReasonCode.SELL_LOW_ORDERS]
    if sell.roi_pct < -30:
        return Action.PAUSE, [f"ROI {sell.roi_pct}% < -30%"], [ReasonCode.SELL_LOW_ROI]
    if sell.roi_pct >= 50 and sell.cvr_pct >= 1.0:
        return Action.SCALE, [f"ROI {sell.roi_pct}% >= 50% + CVR {sell.cvr_pct}% >= 1%"], [ReasonCode.SELL_GOOD_ROI_CVR]
    return Action.HOLD, ["sell metrics insufficient"], []
