"""
Data models for assets, portfolios, scenarios, and results.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from decimal import Decimal


@dataclass
class Asset:
    """Represents a single financial asset."""
    id: str
    currency: str
    value: Decimal


@dataclass
class Portfolio:
    """Represents a collection of assets."""
    assets: List[Asset]
    portfolio_id: Optional[str] = None


@dataclass
class Scenario:
    """Represents a market scenario with various risk factors."""
    market_movement_bps: Decimal
    volatility_change_bps: Decimal
    currency_rate_changes: Dict[str, Decimal]
    interest_rate_change_bps: Decimal
    scenario_id: Optional[str] = None
    scenario_name: Optional[str] = None


@dataclass
class PortfolioResult:
    """Results of applying a scenario to a portfolio."""
    run_id: str
    timestamp: str
    portfolio_id: Optional[str]
    scenario_id: Optional[str]
    base_portfolio_value: Decimal
    adjusted_portfolio_value: Decimal
    value_change: Decimal
    value_change_percent: Decimal
    currency_breakdown: Dict[str, Dict[str, Decimal]]
    risk_metrics: Optional[Dict[str, Decimal]] = None

