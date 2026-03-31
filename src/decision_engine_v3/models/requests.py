"""Input request models — legacy and domain."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class LegacyExplorePayload:
    """Legacy V2 explore request format."""
    views: int = 0
    clicks: int = 0
    ctr: float = 0.0
    saves: int = 0
    save_rate: float = 0.0
    comments: list[str] = field(default_factory=list)
    total_comments: int = 0
    likes: int = 0
    shares: int = 0
    # marketplace
    competitors: int = 0
    avg_price: float = 0.0
    min_price: float = 0.0
    max_price: float = 0.0
    avg_reviews: float = 0.0
    avg_rating: float = 0.0
    top_seller_revenue: float = 0.0
    # economics
    estimated_cost: float = 0.0
    landed_cost: float = 0.0
    target_price: float = 0.0
    market_min_price: float = 0.0
    platform_fee_pct: float = 15.0
    # context
    product_name: str = ""
    category: str = ""
    source: str = ""


@dataclass
class LegacySellPayload:
    """Legacy V2 sell request format."""
    orders: int = 0
    revenue: float = 0.0
    ad_spend: float = 0.0
    roi_pct: float = 0.0
    cvr_pct: float = 0.0
    product_name: str = ""
