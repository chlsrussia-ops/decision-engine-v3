"""Test builders for common payloads."""
from decision_engine_v3.models.requests import LegacyExplorePayload

def good_explore(**overrides) -> LegacyExplorePayload:
    base = dict(
        views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
        comments=["где купить", "сколько стоит", "хочу", "беру", "ссылку",
                   "артикул", "нужно", "заказать", "цена", "доставка",
                   "заказал", "куплю", "хочу подарок", "где дешевле", "доставкой"],
        total_comments=15, likes=200, shares=30, product_name="Test Widget",
    )
    base.update(overrides)
    return LegacyExplorePayload(**base)
