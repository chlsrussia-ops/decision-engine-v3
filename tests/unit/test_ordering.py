from decision_engine_v3.policies.ordering import min_action, max_action, is_positive, is_negative, action_severity
from decision_engine_v3.models.enums import Action

def test_severity_order():
    assert action_severity(Action.NEVER_TEST) < action_severity(Action.HOLD) < action_severity(Action.TEST_PRODUCT) < action_severity(Action.SCALE)

def test_min_action():
    assert min_action(Action.TEST_PRODUCT, Action.HOLD) == Action.HOLD
    assert min_action(Action.DISCARD, Action.HOLD) == Action.DISCARD

def test_max_action():
    assert max_action(Action.HOLD, Action.TEST_PRODUCT) == Action.TEST_PRODUCT

def test_is_positive():
    assert is_positive(Action.TEST_PRODUCT)
    assert is_positive(Action.SCALE)
    assert not is_positive(Action.HOLD)

def test_is_negative():
    assert is_negative(Action.DISCARD)
    assert is_negative(Action.NEVER_TEST)
    assert not is_negative(Action.HOLD)
