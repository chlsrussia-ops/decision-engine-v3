"""Map legacy payloads to domain inputs. No business logic."""
from ..models.requests import LegacyExplorePayload, LegacySellPayload
from ..models.data import ContentMetrics, MarketplaceMetrics, EconomicsPreview, ReviewerContext, SellMetrics


def map_explore_input(p: LegacyExplorePayload) -> tuple[ContentMetrics, MarketplaceMetrics, EconomicsPreview, ReviewerContext]:
    content = ContentMetrics(views=p.views, clicks=p.clicks, ctr=p.ctr, saves=p.saves, save_rate=p.save_rate, comments=p.comments, total_comments=p.total_comments or len(p.comments), likes=p.likes, shares=p.shares)
    marketplace = MarketplaceMetrics(competitors=p.competitors, avg_price=p.avg_price, min_price=p.min_price, max_price=p.max_price, avg_reviews=p.avg_reviews, avg_rating=p.avg_rating, top_seller_revenue_estimate=p.top_seller_revenue)
    economics = EconomicsPreview(estimated_cost=p.estimated_cost, landed_cost=p.landed_cost, target_price=p.target_price, market_min_price=p.market_min_price, platform_fee_pct=p.platform_fee_pct)
    reviewer = ReviewerContext(product_name=p.product_name, category=p.category, source=p.source)
    return content, marketplace, economics, reviewer


def map_sell_input(p: LegacySellPayload) -> SellMetrics:
    return SellMetrics(orders=p.orders, revenue=p.revenue, ad_spend=p.ad_spend, roi_pct=p.roi_pct, cvr_pct=p.cvr_pct)
