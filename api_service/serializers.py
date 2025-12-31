"""
Request/response serialization and validation.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator
from decimal import Decimal


class AssetRequest(BaseModel):
    """Asset in request payload."""
    id: str
    currency: str = Field(..., min_length=3, max_length=3)
    value: float


class PortfolioRequest(BaseModel):
    """Portfolio in request payload."""
    portfolio_id: Optional[str] = None
    assets: List[AssetRequest]


class CurrencyRateChanges(BaseModel):
    """Currency rate changes mapping."""
    __root__: Dict[str, float]


class ScenarioRequest(BaseModel):
    """Scenario in request payload."""
    scenario_id: Optional[str] = None
    scenario_name: Optional[str] = None
    market_movement_bps: float
    volatility_change_bps: float
    currency_rate_changes: Dict[str, float] = Field(default_factory=dict)
    interest_rate_change_bps: float
    
    @validator('market_movement_bps', 'volatility_change_bps', 'interest_rate_change_bps')
    def validate_bps_range(cls, v):
        """Validate basis points are in reasonable range."""
        if v < -10000 or v > 10000:
            raise ValueError(f"BPS value {v} out of range [-10000, 10000]")
        return v


class EvaluationOptions(BaseModel):
    """Options for evaluation."""
    base_currency: str = Field(default="USD", min_length=3, max_length=3)
    include_metrics: List[str] = Field(default_factory=list)


class EvaluationRequest(BaseModel):
    """Request for single evaluation."""
    portfolio: PortfolioRequest
    scenario: ScenarioRequest
    options: EvaluationOptions = Field(default_factory=EvaluationOptions)


class BatchEvaluationRequest(BaseModel):
    """Request for batch evaluation."""
    portfolio: PortfolioRequest
    scenarios: List[ScenarioRequest]
    options: EvaluationOptions = Field(default_factory=EvaluationOptions)


class CurrencyBreakdownItem(BaseModel):
    """Currency breakdown item in response."""
    base_value: str
    adjusted_value: str
    fx_impact: str


class EvaluationResult(BaseModel):
    """Evaluation result in response."""
    base_portfolio_value: str
    adjusted_portfolio_value: str
    value_change: str
    value_change_percent: str
    currency_breakdown: Dict[str, CurrencyBreakdownItem]
    risk_metrics: Optional[Dict[str, str]] = None


class EvaluationResponse(BaseModel):
    """Response for single evaluation."""
    run_id: str
    timestamp: str
    result: EvaluationResult
    csv_download_url: str


class RunListItem(BaseModel):
    """Single run item in list response."""
    run_id: str
    timestamp: str
    portfolio_id: Optional[str]
    scenario_id: Optional[str]
    base_portfolio_value: str
    adjusted_portfolio_value: str
    value_change: str
    value_change_percent: str


class RunListResponse(BaseModel):
    """Response for list of runs."""
    runs: List[RunListItem]
    total: int
    page: int
    limit: int

