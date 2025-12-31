"""
Main batch processing logic for evaluating portfolios against scenarios.
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from decimal import Decimal

from risk_core.models import Portfolio, Scenario, PortfolioResult, Asset
from risk_core.portfolio import PortfolioManager
from risk_core.scenario import ScenarioApplicator
from risk_core.currency import CurrencyConverter
from risk_core.calculations import calculate_value_change_percent
from batch_processor.file_reader import JSONFileReader, FileReaderError
from batch_processor.logger import get_logger

logger = get_logger(__name__)


class BatchProcessor:
    """Main processor for batch evaluation of portfolios against scenarios."""
    
    def __init__(self, base_currency: str = "USD"):
        """
        Initialize batch processor.
        
        Args:
            base_currency: Base currency for calculations (default: USD)
        """
        self.base_currency = base_currency
        self.currency_converter = CurrencyConverter()
    
    def process(
        self,
        portfolio_file: Path,
        scenarios_file: Path,
        output_file: Path
    ) -> str:
        """
        Process portfolio against scenarios and generate CSV output.
        
        Args:
            portfolio_file: Path to portfolio JSON file
            scenarios_file: Path to scenarios JSON file
            output_file: Path to output CSV file
            
        Returns:
            Run ID (UUID) for this processing run
            
        Raises:
            FileReaderError: If input files cannot be read
        """
        run_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Starting batch processing run {run_id}")
        
        try:
            # Read portfolio
            logger.info(f"Reading portfolio from {portfolio_file}")
            portfolio = JSONFileReader.read_portfolio(portfolio_file)
            
            # Read scenarios
            logger.info(f"Reading scenarios from {scenarios_file}")
            scenarios = JSONFileReader.read_scenarios(scenarios_file)
            
            # Process each scenario
            results = []
            for scenario in scenarios:
                logger.info(f"Processing scenario: {scenario.scenario_id or 'unnamed'}")
                result = self._evaluate_portfolio(portfolio, scenario, run_id, timestamp)
                results.append(result)
            
            # Write CSV output
            logger.info(f"Writing results to {output_file}")
            from batch_processor.csv_writer import CSVWriter
            csv_writer = CSVWriter()
            csv_writer.write_results(results, output_file)
            
            logger.info(f"Batch processing completed: {run_id}")
            return run_id
            
        except Exception as e:
            logger.error(f"Error in batch processing run {run_id}: {e}")
            raise
    
    def _evaluate_portfolio(
        self,
        portfolio: Portfolio,
        scenario: Scenario,
        run_id: str,
        timestamp: str
    ) -> PortfolioResult:
        """
        Evaluate a portfolio against a scenario.
        
        Args:
            portfolio: Portfolio to evaluate
            scenario: Scenario to apply
            run_id: Unique run identifier
            timestamp: ISO timestamp for the run
            
        Returns:
            PortfolioResult with calculated metrics
        """
        # Calculate base portfolio value
        portfolio_manager = PortfolioManager(portfolio)
        base_breakdown = portfolio_manager.currency_breakdown()
        
        # Convert to base currency
        base_portfolio_value = Decimal('0')
        for currency, value in base_breakdown.items():
            if currency == self.base_currency:
                base_portfolio_value += value
            else:
                converted_value = self.currency_converter.convert(
                    value, currency, self.base_currency
                )
                base_portfolio_value += converted_value
        
        # Apply scenario
        scenario_applicator = ScenarioApplicator(scenario)
        adjusted_values = scenario_applicator.apply_to_portfolio(
            portfolio, self.base_currency
        )
        
        # Calculate adjusted portfolio value
        adjusted_portfolio_value = Decimal('0')
        currency_breakdown = {}
        
        for asset in portfolio.assets:
            adjusted_value = adjusted_values[asset.id]
            adjusted_portfolio_value += adjusted_value
            
            # Track currency breakdown
            if asset.currency not in currency_breakdown:
                currency_breakdown[asset.currency] = {
                    'base_value': Decimal('0'),
                    'adjusted_value': Decimal('0')
                }
            currency_breakdown[asset.currency]['base_value'] += asset.value
            currency_breakdown[asset.currency]['adjusted_value'] += adjusted_value
        
        # Calculate changes
        value_change = adjusted_portfolio_value - base_portfolio_value
        value_change_percent = calculate_value_change_percent(
            base_portfolio_value, adjusted_portfolio_value
        )
        
        # Calculate FX impacts for currency breakdown
        for currency, breakdown in currency_breakdown.items():
            if currency != self.base_currency:
                base_in_base = self.currency_converter.convert(
                    breakdown['base_value'], currency, self.base_currency
                )
                adjusted_in_base = self.currency_converter.convert(
                    breakdown['adjusted_value'], currency, self.base_currency,
                    scenario.currency_rate_changes.get(currency, Decimal('0'))
                )
                breakdown['fx_impact'] = adjusted_in_base - base_in_base
            else:
                breakdown['fx_impact'] = Decimal('0')
        
        return PortfolioResult(
            run_id=run_id,
            timestamp=timestamp,
            portfolio_id=portfolio.portfolio_id,
            scenario_id=scenario.scenario_id,
            base_portfolio_value=base_portfolio_value,
            adjusted_portfolio_value=adjusted_portfolio_value,
            value_change=value_change,
            value_change_percent=value_change_percent,
            currency_breakdown=currency_breakdown,
            risk_metrics=None  # TODO: Calculate risk metrics if needed
        )

