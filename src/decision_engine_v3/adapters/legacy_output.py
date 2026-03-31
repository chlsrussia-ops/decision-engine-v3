"""Map Decision → backward-compatible response dict."""
from ..models.responses import decision_to_legacy_response
from ..models.data import Decision


def build_legacy_response(decision: Decision) -> dict:
    return decision_to_legacy_response(decision)
