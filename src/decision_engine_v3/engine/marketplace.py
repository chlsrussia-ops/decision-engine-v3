"""Marketplace Modifier — read-only sanity check. Never upgrades."""
from __future__ import annotations
from ..models.data import MarketplaceModifierResult, MarketplaceMetrics


def compute_marketplace(m: MarketplaceMetrics | None) -> MarketplaceModifierResult:
    if not m or m.competitors == 0:
        return MarketplaceModifierResult(saturation_state="unknown", review_maturity="unknown")

    demand_proof = min(m.top_seller_revenue_estimate / 50000.0, 1.0) if m.top_seller_revenue_estimate > 0 else 0.0
    pressure = min(m.competitors / 100.0, 1.0)
    sat = "virgin" if m.competitors < 5 else "emerging" if m.competitors < 20 else "growing" if m.competitors < 50 else "mature" if m.competitors < 100 else "saturated" if m.competitors < 200 else "dead"
    rev_mat = "no_reviews" if m.avg_reviews < 1 else "few" if m.avg_reviews < 10 else "moderate" if m.avg_reviews < 50 else "established" if m.avg_reviews < 200 else "mature"
    price_range = m.max_price - m.min_price if m.max_price > m.min_price else 0
    price_compression = round(1.0 - min(price_range / max(m.avg_price, 1), 1.0), 4) if m.avg_price > 0 else 0.0
    price_risk = round(price_compression * pressure, 4)
    fake_opp = 0.0
    if sat == "dead" and demand_proof < 0.2:
        fake_opp = 0.8
    elif sat == "saturated" and price_compression > 0.7:
        fake_opp = 0.6

    viability_adj = 0.0
    caution = []
    block = False
    if sat == "dead":
        viability_adj = -0.15; caution.append("dead_market")
    if pressure > 0.7:
        viability_adj -= 0.05; caution.append("high_pressure")
    if price_compression > 0.8:
        caution.append("price_compressed")
    if fake_opp > 0.5:
        caution.append("possible_fake_opportunity")

    return MarketplaceModifierResult(
        demand_proof_score=round(demand_proof, 4), pressure_score=round(pressure, 4),
        saturation_state=sat, review_maturity=rev_mat,
        price_compression=price_compression, price_risk=price_risk,
        fake_opportunity=round(fake_opp, 4), margin_precheck="unknown",
        viability_adjustment=round(viability_adj, 4),
        caution_reasons=caution, block=block,
    )
