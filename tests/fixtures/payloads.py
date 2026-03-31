"""Shared test fixtures."""
from decision_engine_v3.models.requests import LegacyExplorePayload, LegacySellPayload

GOOD_EXPLORE = LegacyExplorePayload(
    views=3000, clicks=60, ctr=0.02, saves=90, save_rate=0.03,
    comments=["где купить", "сколько стоит", "хочу", "беру", "ссылку дай",
              "артикул", "нужно", "как заказать", "цена", "доставка",
              "заказал", "куплю", "хочу на подарок", "где дешевле", "с доставкой"],
    total_comments=15, likes=200, shares=30,
    competitors=25, avg_price=1500, min_price=800, max_price=2500, avg_reviews=45,
    target_price=1500, landed_cost=500, estimated_cost=400, market_min_price=700,
    product_name="Smart Gadget",
)

WEAK_EXPLORE = LegacyExplorePayload(
    views=200, clicks=3, ctr=0.015, saves=2, save_rate=0.01,
    comments=["прикольно", "вау"], total_comments=2,
    product_name="Weak Signal",
)

VIRAL_TRASH = LegacyExplorePayload(
    views=50000, clicks=100, ctr=0.002, saves=200, save_rate=0.004,
    comments=["вау"] * 20, total_comments=20,
    product_name="Viral Trash",
)

GOOD_SELL = LegacySellPayload(orders=50, revenue=75000, ad_spend=15000, roi_pct=60, cvr_pct=2.0)
BAD_SELL = LegacySellPayload(orders=10, revenue=5000, ad_spend=10000, roi_pct=-50, cvr_pct=0.3)
