"""
JSON input parsing and validation.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from decimal import Decimal

from risk_core.models import Asset, Portfolio, Scenario
from risk_core.validators import validate_portfolio, validate_scenario, ValidationError


class FileReaderError(Exception):
    """Raised when file reading or parsing fails."""
    pass


class JSONFileReader:
    """Reads and parses JSON input files for portfolios and scenarios."""
    
    @staticmethod
    def read_portfolio(file_path: Path) -> Portfolio:
        """
        Read and parse a portfolio JSON file.
        
        Args:
            file_path: Path to portfolio JSON file
            
        Returns:
            Portfolio object
            
        Raises:
            FileReaderError: If file cannot be read or parsed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse assets
            assets = []
            for asset_data in data.get('assets', []):
                asset = Asset(
                    id=asset_data['id'],
                    currency=asset_data['currency'],
                    value=Decimal(str(asset_data['value']))
                )
                assets.append(asset)
            
            portfolio = Portfolio(
                assets=assets,
                portfolio_id=data.get('portfolio_id')
            )
            
            # Validate portfolio
            validate_portfolio(portfolio)
            
            return portfolio
            
        except FileNotFoundError:
            raise FileReaderError(f"Portfolio file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise FileReaderError(f"Invalid JSON in portfolio file: {e}")
        except KeyError as e:
            raise FileReaderError(f"Missing required field in portfolio: {e}")
        except ValidationError as e:
            raise FileReaderError(f"Portfolio validation error: {e}")
    
    @staticmethod
    def read_scenario(file_path: Path) -> Scenario:
        """
        Read and parse a scenario JSON file.
        
        Args:
            file_path: Path to scenario JSON file
            
        Returns:
            Scenario object
            
        Raises:
            FileReaderError: If file cannot be read or parsed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse currency rate changes
            currency_rate_changes = {}
            for currency, rate_change in data.get('currency_rate_changes', {}).items():
                currency_rate_changes[currency] = Decimal(str(rate_change))
            
            scenario = Scenario(
                market_movement_bps=Decimal(str(data['market_movement_bps'])),
                volatility_change_bps=Decimal(str(data['volatility_change_bps'])),
                currency_rate_changes=currency_rate_changes,
                interest_rate_change_bps=Decimal(str(data['interest_rate_change_bps'])),
                scenario_id=data.get('scenario_id'),
                scenario_name=data.get('scenario_name')
            )
            
            # Validate scenario
            validate_scenario(scenario)
            
            return scenario
            
        except FileNotFoundError:
            raise FileReaderError(f"Scenario file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise FileReaderError(f"Invalid JSON in scenario file: {e}")
        except KeyError as e:
            raise FileReaderError(f"Missing required field in scenario: {e}")
        except ValidationError as e:
            raise FileReaderError(f"Scenario validation error: {e}")
    
    @staticmethod
    def read_scenarios(file_path: Path) -> List[Scenario]:
        """
        Read and parse multiple scenarios from a JSON file.
        The file should contain a list of scenarios or a single scenario object.
        
        Args:
            file_path: Path to scenarios JSON file
            
        Returns:
            List of Scenario objects
            
        Raises:
            FileReaderError: If file cannot be read or parsed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            scenarios = []
            
            # Check if it's a list of scenarios
            if isinstance(data, list):
                for scenario_data in data:
                    scenario = JSONFileReader._parse_scenario_data(scenario_data)
                    scenarios.append(scenario)
            # Or a single scenario object
            elif isinstance(data, dict):
                scenario = JSONFileReader._parse_scenario_data(data)
                scenarios.append(scenario)
            else:
                raise FileReaderError("Scenarios file must contain a list or object")
            
            return scenarios
            
        except FileNotFoundError:
            raise FileReaderError(f"Scenarios file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise FileReaderError(f"Invalid JSON in scenarios file: {e}")
    
    @staticmethod
    def _parse_scenario_data(data: Dict[str, Any]) -> Scenario:
        """Parse scenario data from dictionary."""
        currency_rate_changes = {}
        for currency, rate_change in data.get('currency_rate_changes', {}).items():
            currency_rate_changes[currency] = Decimal(str(rate_change))
        
        scenario = Scenario(
            market_movement_bps=Decimal(str(data['market_movement_bps'])),
            volatility_change_bps=Decimal(str(data['volatility_change_bps'])),
            currency_rate_changes=currency_rate_changes,
            interest_rate_change_bps=Decimal(str(data['interest_rate_change_bps'])),
            scenario_id=data.get('scenario_id'),
            scenario_name=data.get('scenario_name')
        )
        
        validate_scenario(scenario)
        return scenario

