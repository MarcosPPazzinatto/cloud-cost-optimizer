# tests/test_discounts.py
from src.pricing.models import DiscountConfig, PurchaseOption, CommitmentTerm
from src.pricing.discounts import effective_hourly_rate


def test_on_demand_no_discount():
    rate = effective_hourly_rate(1.0, None)
    assert rate == 1.0


def test_explicit_discount():
    d = DiscountConfig(
        purchase=PurchaseOption.SAVINGS_PLAN,
        commitment=CommitmentTerm.ONE_YEAR,
        effective_discount_pct=0.3
    )
    rate = effective_hourly_rate(1.0, d)
    assert abs(rate - 0.7) < 1e-9


def test_clamped_discount():
    d = DiscountConfig(
        purchase=PurchaseOption.SPOT,
        commitment=CommitmentTerm.NONE,
        effective_discount_pct=0.999
    )
    rate = effective_hourly_rate(2.0, d)
    # clamped to 0.95 -> effective rate is 2 * (1 - 0.95) = 0.1
    assert abs(rate - 0.1) < 1e-9


def test_fallback_defaults_do_not_raise():
    # no effective discount provided -> use safe fallback
    d = DiscountConfig(
        purchase=PurchaseOption.CUD,
        commitment=CommitmentTerm.THREE_YEARS
    )
    rate = effective_hourly_rate(10.0, d)
    assert 0.0 < rate < 10.0

