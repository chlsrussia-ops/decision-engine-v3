"""Action ordering helpers — deterministic severity comparison."""
from ..models.enums import Action

_SEVERITY = {
    Action.NEVER_TEST: 0, Action.DISCARD: 1, Action.PAUSE: 2,
    Action.HOLD: 3, Action.CAUTION: 4, Action.TEST_PRODUCT: 5, Action.SCALE: 6,
}


def action_severity(action: Action) -> int:
    return _SEVERITY.get(action, 3)


def min_action(a: Action, b: Action) -> Action:
    """Return the more conservative (lower severity) action."""
    return a if action_severity(a) <= action_severity(b) else b


def max_action(a: Action, b: Action) -> Action:
    """Return the more permissive (higher severity) action."""
    return a if action_severity(a) >= action_severity(b) else b


def is_positive(action: Action) -> bool:
    return action in (Action.TEST_PRODUCT, Action.SCALE)


def is_negative(action: Action) -> bool:
    return action in (Action.NEVER_TEST, Action.DISCARD, Action.PAUSE)
