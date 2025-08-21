# src/pricing/models.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any


class PurchaseOption(str, Enum):
    ON_DEMAND = "on_demand"
    SPOT = "spot"                 # AWS Spot / GCP Preemptible
    RESERVED = "reserved"         # AWS RI
    SAVINGS_PLAN = "savings_plan" # AWS Savings Plan
    CUD = "cud"                   # GCP Committed Use Discount


class CommitmentTerm(str, Enum):
    NONE = "none"
    ONE_YEAR = "1y"
    THREE_YEARS = "3y"


@dataclass
class DiscountConfig:
    purchase: PurchaseOption = PurchaseOption.ON_DEMAND
    commitment: CommitmentTerm = CommitmentTerm.NONE
    # Effective discount as a percentage in [0.0, 1.0], applied on top of base on-demand rate.
    # Example: 0.35 = 35% cheaper than on-demand.
    effective_discount_pct: Optional[float] = None
    # Optional provider-specific knobs for future expansion (e.g., SP type, RI class, scope)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourcePricingInput:
    provider: str                # "aws" or "gcp"
    region: str
    base_hourly_rate: float      # on-demand base hourly price for the resource
    discounts: Optional[DiscountConfig] = None

