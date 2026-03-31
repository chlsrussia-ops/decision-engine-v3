"""Economics Engine — margin checks."""
from __future__ import annotations
from ..models.data import EconomicsResult, EconomicsPreview


def compute_economics(e: EconomicsPreview | None) -> EconomicsResult:
    if not e or e.target_price <= 0:
        return EconomicsResult(status="unknown")
    margin = round((e.target_price - e.landed_cost - e.target_price * e.platform_fee_pct / 100) / e.target_price * 100, 2)
    landed_above = e.landed_cost > e.market_min_price if e.market_min_price > 0 else False
    ok = margin >= 10.0 and not landed_above
    status = "ok" if ok else "fail" if margin < 10.0 or landed_above else "warning"
    return EconomicsResult(estimated_margin_pct=margin, margin_ok=ok, landed_above_market_min=landed_above, status=status)
