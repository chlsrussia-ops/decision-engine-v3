"""Payload validation — reject or safely default malformed inputs."""
from ..models.requests import LegacyExplorePayload, LegacySellPayload


class PayloadValidationError(Exception):
    pass


def validate_explore_payload(p: LegacyExplorePayload) -> list[str]:
    errors = []
    if p.views < 0: errors.append("views cannot be negative")
    if p.clicks < 0: errors.append("clicks cannot be negative")
    if p.ctr < 0: errors.append("ctr cannot be negative")
    if p.save_rate < 0: errors.append("save_rate cannot be negative")
    return errors


def validate_sell_payload(p: LegacySellPayload) -> list[str]:
    errors = []
    if p.orders < 0: errors.append("orders cannot be negative")
    return errors
