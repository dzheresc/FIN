"""
Scenario application logic for market movements, volatility, FX, and interest rates.
"""

from decimal import Decimal
from typing import Dict
from .models import Asset, Scenario, Portfolio


class ScenarioApplicator:
    """Applies scenarios to assets and portfolios."""
    
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
    
    def apply_to_asset(self, asset: Asset, base_currency: str) -> Decimal:
        """
        Apply scenario to a single asset.
        
        Args:
            asset: Asset to apply scenario to
            base_currency: Base currency for calculations
            
        Returns:
            Adjusted asset value
        """
        # Start with base value
        adjusted_value = asset.value
        
        # Apply market movement
        adjusted_value = self._apply_market_movement(adjusted_value)
        
        # Apply volatility adjustment
        adjusted_value = self._apply_volatility_adjustment(adjusted_value)
        
        # Apply currency rate changes if applicable
        if asset.currency != base_currency:
            adjusted_value = self._apply_currency_change(
                adjusted_value, asset.currency, base_currency
            )
        
        return adjusted_value
    
    def apply_to_portfolio(self, portfolio: Portfolio, base_currency: str) -> Dict[str, Decimal]:
        """
        Apply scenario to entire portfolio.
        
        Args:
            portfolio: Portfolio to apply scenario to
            base_currency: Base currency for calculations
            
        Returns:
            Dictionary mapping asset IDs to adjusted values
        """
        results = {}
        for asset in portfolio.assets:
            results[asset.id] = self.apply_to_asset(asset, base_currency)
        return results
    
    def _apply_market_movement(self, value: Decimal) -> Decimal:
        """Apply market movement in basis points."""
        movement_factor = Decimal('1') + (self.scenario.market_movement_bps / Decimal('10000'))
        return value * movement_factor
    
    def _apply_volatility_adjustment(self, value: Decimal) -> Decimal:
        """Apply volatility change adjustment."""
        # TODO: Implement volatility scaling logic
        volatility_factor = Decimal('1') + (self.scenario.volatility_change_bps / Decimal('10000'))
        return value * volatility_factor
    
    def _apply_currency_change(
        self, value: Decimal, from_currency: str, to_currency: str
    ) -> Decimal:
        """Apply currency rate changes."""
        # TODO: Implement currency conversion with rate changes
        # Check if currency rate change exists for from_currency
        if from_currency in self.scenario.currency_rate_changes:
            rate_change_bps = self.scenario.currency_rate_changes[from_currency]
            rate_factor = Decimal('1') + (rate_change_bps / Decimal('10000'))
            return value * rate_factor
        return value

