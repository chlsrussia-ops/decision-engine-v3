from decision_engine_v3.engine.core import DecisionEngineV3
from decision_engine_v3.models.data import ContentMetrics
from decision_engine_v3.models.enums import Action

def test_zero_comments():
    e = DecisionEngineV3()
    d = e.decide_explore(ContentMetrics(views=1000, clicks=20, ctr=0.02, save_rate=0.03, saves=30, comments=[], total_comments=0))
    assert d.action == Action.HOLD

def test_all_duplicates():
    e = DecisionEngineV3()
    d = e.decide_explore(ContentMetrics(views=2000, clicks=40, ctr=0.02, save_rate=0.03, saves=60, comments=["хочу"] * 50, total_comments=50))
    # High dedup → low confidence → capped
    assert d.action in (Action.HOLD, Action.CAUTION, Action.TEST_PRODUCT)

def test_missing_marketplace():
    e = DecisionEngineV3()
    d = e.decide_explore(ContentMetrics(views=3000, clicks=60, ctr=0.02, save_rate=0.03, saves=90, comments=["где купить"] * 15, total_comments=15), marketplace_raw=None)
    assert d.action is not None
    assert d.degraded is False  # marketplace=None is normal, not degradation
