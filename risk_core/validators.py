"""
Input validation functions for assets, portfolios, and scenarios.
"""

from decimal import Decimal
from typing import List, Dict
from .models import Asset, Portfolio, Scenario


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_currency_code(currency: str) -> bool:
    """
    Validate currency code format (ISO 4217).
    
    Args:
        currency: Currency code to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If currency code is invalid
    """
    if not currency or len(currency) != 3:
        raise ValidationError(f"Invalid currency code: {currency}. Must be 3 characters (ISO 4217)")
    
    if not currency.isalpha() or not currency.isupper():
        raise ValidationError(f"Invalid currency code: {currency}. Must be uppercase letters")
    
    return True


def validate_asset(asset: Asset) -> None:
    """
    Validate an asset object.
    
    Args:
        asset: Asset to validate
        
    Raises:
        ValidationError: If asset is invalid
    """
    if not asset.id or not asset.id.strip():
        raise ValidationError("Asset ID cannot be empty")
    
    validate_currency_code(asset.currency)
    
    if asset.value < Decimal('0'):
        raise ValidationError(f"Asset value cannot be negative: {asset.value}")


def validate_portfolio(portfolio: Portfolio) -> None:
    """
    Validate a portfolio object.
    
    Args:
        portfolio: Portfolio to validate
        
    Raises:
        ValidationError: If portfolio is invalid
    """
    if not portfolio.assets:
        raise ValidationError("Portfolio must contain at least one asset")
    
    asset_ids = set()
    for asset in portfolio.assets:
        validate_asset(asset)
        
        if asset.id in asset_ids:
            raise ValidationError(f"Duplicate asset ID: {asset.id}")
        asset_ids.add(asset.id)


def validate_scenario(scenario: Scenario) -> None:
    """
    Validate a scenario object.
    
    Args:
        scenario: Scenario to validate
        
    Raises:
        ValidationError: If scenario is invalid
    """
    # Validate basis points are within reasonable range
    # Typically -10000 to +10000 bps (-100% to +100%)
    max_bps = Decimal('10000')
    min_bps = Decimal('-10000')
    
    if scenario.market_movement_bps < min_bps or scenario.market_movement_bps > max_bps:
        raise ValidationError(
            f"Market movement BPS out of range: {scenario.market_movement_bps}. "
            f"Must be between {min_bps} and {max_bps}"
        )
    
    if scenario.volatility_change_bps < min_bps or scenario.volatility_change_bps > max_bps:
        raise ValidationError(
            f"Volatility change BPS out of range: {scenario.volatility_change_bps}. "
            f"Must be between {min_bps} and {max_bps}"
        )
    
    if scenario.interest_rate_change_bps < min_bps or scenario.interest_rate_change_bps > max_bps:
        raise ValidationError(
            f"Interest rate change BPS out of range: {scenario.interest_rate_change_bps}. "
            f"Must be between {min_bps} and {max_bps}"
        )
    
    # Validate currency rate changes
    for currency, rate_change in scenario.currency_rate_changes.items():
        validate_currency_code(currency)
        if rate_change < min_bps or rate_change > max_bps:
            raise ValidationError(
                f"Currency rate change BPS for {currency} out of range: {rate_change}. "
                f"Must be between {min_bps} and {max_bps}"
            )

