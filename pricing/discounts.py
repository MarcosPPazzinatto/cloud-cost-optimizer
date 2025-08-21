# src/pricing/discounts.py
from .models import DiscountConfig, PurchaseOption, CommitmentTerm


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _fallback_defaults(discount: DiscountConfig) -> float:
    """
    Neutral, conservative defaults when no effective_discount_pct is provided.
    These are placeholders to enable the flow without hardcoding vendor-specific rates.
    Teams should set 'effective_discount_pct' per workload/contract to reflect real deals.
    """
    if discount.purchase == PurchaseOption.ON_DEMAND:
        return 0.0

    # Conservative placeholders (feel free to tune per account reality):
    if discount.purchase == PurchaseOption.SPOT:
        # Spot/Preemptible varies widely. Start conservative.
        return 0.3  # 30% cheaper than on-demand

    if discount.purchase in (PurchaseOption.RESERVED, PurchaseOption.SAVINGS_PLAN, PurchaseOption.CUD):
        # 1y vs 3y: stronger discount for longer commitments
        if discount.commitment == CommitmentTerm.THREE_YEARS:
            return 0.4
        if discount.commitment == CommitmentTerm.ONE_YEAR:
            return 0.25
        return 0.15

    return 0.0


def effective_hourly_rate(base_hourly_rate: float, discount: DiscountConfig | None) -> float:
    """
    Returns the effective hourly rate after applying discounts.
    If 'effective_discount_pct' is provided, use it directly (clamped to [0,1]).
    Otherwise, apply neutral fallback defaults.
    """
    if discount is None:
        return base_hourly_rate

    pct = discount.effective_discount_pct
    if pct is None:
        pct = _fallback_defaults(discount)

    pct = clamp(pct, 0.0, 0.95)  # safety clamp; avoid zero/negative pricing
    return base_hourly_rate * (1.0 - pct)

