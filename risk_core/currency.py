"""
Currency conversion utilities and rate management.
"""

from decimal import Decimal
from typing import Dict, Optional


class CurrencyConverter:
    """Handles currency conversions with rate changes."""
    
    def __init__(self, base_rates: Optional[Dict[str, Decimal]] = None):
        """
        Initialize currency converter.
        
        Args:
            base_rates: Dictionary of base exchange rates (to USD by default)
                       Format: {"EUR": 1.10, "GBP": 1.25, ...}
        """
        self.base_rates = base_rates or self._get_default_rates()
    
    def convert(
        self,
        value: Decimal,
        from_currency: str,
        to_currency: str,
        rate_change_bps: Decimal = Decimal('0')
    ) -> Decimal:
        """
        Convert value from one currency to another with optional rate change.
        
        Args:
            value: Value to convert
            from_currency: Source currency code (ISO 4217)
            to_currency: Target currency code (ISO 4217)
            rate_change_bps: Rate change in basis points
            
        Returns:
            Converted value
        """
        if from_currency == to_currency:
            return value
        
        # Get base rates
        from_rate = self.base_rates.get(from_currency, Decimal('1'))
        to_rate = self.base_rates.get(to_currency, Decimal('1'))
        
        # Apply rate change
        if rate_change_bps != Decimal('0'):
            rate_factor = Decimal('1') + (rate_change_bps / Decimal('10000'))
            from_rate = from_rate * rate_factor
        
        # Convert: value_in_usd = value / from_rate
        # Then: value_in_target = value_in_usd * to_rate
        value_in_usd = value / from_rate
        value_in_target = value_in_usd * to_rate
        
        return value_in_target
    
    def get_base_rates(self) -> Dict[str, Decimal]:
        """
        Get current base exchange rates.
        
        Returns:
            Dictionary of currency codes to exchange rates
        """
        return self.base_rates.copy()
    
    def _get_default_rates(self) -> Dict[str, Decimal]:
        """
        Get default exchange rates (to USD).
        These are example rates and should be replaced with real data.
        
        Returns:
            Dictionary of default rates
        """
        return {
            "USD": Decimal('1.0'),
            "EUR": Decimal('1.10'),
            "GBP": Decimal('1.25'),
            "JPY": Decimal('0.0067'),
            "CHF": Decimal('1.12'),
            "CAD": Decimal('0.74'),
            "AUD": Decimal('0.65'),
        }
    
    def update_rates(self, new_rates: Dict[str, Decimal]) -> None:
        """
        Update base exchange rates.
        
        Args:
            new_rates: Dictionary of currency codes to new rates
        """
        self.base_rates.update(new_rates)

