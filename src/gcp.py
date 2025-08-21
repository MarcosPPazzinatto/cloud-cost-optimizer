# src/gcp.py
from typing import Dict, Any
from .pricing.models import ResourcePricingInput, DiscountConfig, PurchaseOption, CommitmentTerm
from .pricing.discounts import effective_hourly_rate


def price_compute_engine(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    params expected:
      {
        "region": "us-central1",
        "base_hourly_rate": 0.094,  # on-demand for chosen machine type
        "discounts": {
            "purchase": "on_demand|spot|cud",
            "commitment": "none|1y|3y",
            "effective_discount_pct": 0.30,          # optional
            "attributes": {"cud_scope": "region"}    # optional
        }
      }
    """
    discounts = None
    if "discounts" in params and params["discounts"]:
        d = params["discounts"]
        discounts = DiscountConfig(
            purchase=PurchaseOption(d.get("purchase", "on_demand")),
            commitment=CommitmentTerm(d.get("commitment", "none")),
            effective_discount_pct=d.get("effective_discount_pct"),
            attributes=d.get("attributes", {}) or {},
        )

    rpi = ResourcePricingInput(
        provider="gcp",
        region=params["region"],
        base_hourly_rate=float(params["base_hourly_rate"]),
        discounts=discounts
    )

    rate = effective_hourly_rate(rpi.base_hourly_rate, rpi.discounts)
    monthly = rate * 730.0

    return {
        "provider": "gcp",
        "region": rpi.region,
        "base_hourly_rate": rpi.base_hourly_rate,
        "effective_hourly_rate": rate,
        "monthly_estimate": monthly,
        "applied_purchase_option": discounts.purchase.value if discounts else "on_demand",
        "applied_commitment": discounts.commitment.value if discounts else "none",
        "applied_discount_pct": (discounts.effective_discount_pct
                                 if discounts and discounts.effective_discount_pct is not None else None)
    }

