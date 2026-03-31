from decision_engine_v3.engine.core import DecisionEngineV3
from decision_engine_v3.models.data import ContentMetrics, SellMetrics
from decision_engine_v3.models.enums import Action

def test_low_save_never_test():
    e = DecisionEngineV3()
    d = e.decide_explore(ContentMetrics(views=5000, clicks=100, ctr=0.02, save_rate=0.005, saves=25, comments=["хочу"]*10, total_comments=10))
    assert d.action == Action.NEVER_TEST

def test_viral_trash_discard():
    e = DecisionEngineV3()
    d = e.decide_explore(ContentMetrics(views=10000, clicks=20, ctr=0.002, save_rate=0.015, saves=150, comments=["вау"]*20, total_comments=20))
    assert d.action in (Action.DISCARD, Action.HOLD)

def test_good_intent_ctr():
    e = DecisionEngineV3()
    comments = [
        "где купить этот товар", "сколько стоит такой", "ссылку дайте", "хочу такой же",
        "артикул скиньте", "беру два", "нужно срочно", "как заказать",
        "цена какая", "доставка есть", "заказал уже", "куплю завтра",
        "где купить дешевле", "сколько стоит с доставкой", "хочу на подарок",
    ]
    d = e.decide_explore(ContentMetrics(views=3000, clicks=60, ctr=0.02, save_rate=0.03, saves=90, comments=comments, total_comments=15))
    assert d.action in (Action.TEST_PRODUCT, Action.CAUTION), f"Got {d.action}, caps={d.caps.reasons}, conf={d.confidence}"

def test_weak_evidence_hold():
    e = DecisionEngineV3()
    d = e.decide_explore(ContentMetrics(views=200, clicks=5, ctr=0.025, save_rate=0.02, saves=4, comments=["где купить"]*3, total_comments=3))
    assert d.action == Action.HOLD

def test_sell_pause():
    e = DecisionEngineV3()
    d = e.decide_sell(SellMetrics(orders=10, roi_pct=-40, cvr_pct=0.5))
    assert d.action == Action.PAUSE

def test_sell_scale():
    e = DecisionEngineV3()
    d = e.decide_sell(SellMetrics(orders=50, roi_pct=60, cvr_pct=2.0))
    assert d.action == Action.SCALE

def test_sell_hold_low_orders():
    e = DecisionEngineV3()
    d = e.decide_sell(SellMetrics(orders=3, roi_pct=100, cvr_pct=5.0))
    assert d.action == Action.HOLD
