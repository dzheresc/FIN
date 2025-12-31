"""
CSV output generation for evaluation results.
"""

import csv
from pathlib import Path
from typing import List
from decimal import Decimal

from risk_core.models import PortfolioResult, Asset, Portfolio, Scenario
from batch_processor.logger import get_logger

logger = get_logger(__name__)


class CSVWriter:
    """Writes evaluation results to CSV files."""
    
    CSV_HEADERS = [
        'run_id',
        'timestamp',
        'portfolio_id',
        'scenario_id',
        'asset_id',
        'currency',
        'base_value',
        'adjusted_value',
        'value_change',
        'value_change_percent',
        'fx_impact',
        'market_impact',
        'volatility_impact'
    ]
    
    def write_results(self, results: List[PortfolioResult], output_file: Path) -> None:
        """
        Write portfolio results to CSV file.
        
        Args:
            results: List of PortfolioResult objects
            output_file: Path to output CSV file
        """
        logger.info(f"Writing {len(results)} result(s) to {output_file}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(self.CSV_HEADERS)
            
            # Write rows for each result
            for result in results:
                self._write_result_rows(writer, result)
        
        logger.info(f"CSV file written successfully: {output_file}")
    
    def _write_result_rows(self, writer: csv.writer, result: PortfolioResult) -> None:
        """
        Write rows for a single portfolio result.
        
        Args:
            writer: CSV writer object
            result: PortfolioResult to write
        """
        # TODO: This needs access to the original portfolio and scenario
        # to write asset-level details. For now, write portfolio-level summary.
        # In full implementation, this would iterate through assets.
        
        # Write portfolio-level summary row
        row = [
            result.run_id,
            result.timestamp,
            result.portfolio_id or '',
            result.scenario_id or '',
            'PORTFOLIO_TOTAL',  # Asset ID placeholder
            '',  # Currency (multi-currency)
            str(result.base_portfolio_value),
            str(result.adjusted_portfolio_value),
            str(result.value_change),
            str(result.value_change_percent),
            '',  # FX impact (calculated per currency)
            '',  # Market impact (calculated per asset)
            ''   # Volatility impact (calculated per asset)
        ]
        writer.writerow(row)
        
        # TODO: Write individual asset rows
        # This requires storing asset-level results in PortfolioResult
        # or passing portfolio/scenario to this method
    
    def write_result_with_assets(
        self,
        result: PortfolioResult,
        portfolio: Portfolio,
        scenario: Scenario,
        asset_results: dict,
        output_file: Path
    ) -> None:
        """
        Write detailed results including asset-level breakdown.
        
        Args:
            result: PortfolioResult object
            portfolio: Original portfolio
            scenario: Applied scenario
            asset_results: Dictionary mapping asset IDs to adjusted values
            output_file: Path to output CSV file
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.CSV_HEADERS)
            
            # Write asset-level rows
            for asset in portfolio.assets:
                adjusted_value = asset_results.get(asset.id, asset.value)
                value_change = adjusted_value - asset.value
                value_change_percent = (
                    (value_change / asset.value * Decimal('100'))
                    if asset.value != Decimal('0') else Decimal('0')
                )
                
                # Calculate FX impact
                fx_impact = Decimal('0')
                if asset.currency in scenario.currency_rate_changes:
                    rate_change_bps = scenario.currency_rate_changes[asset.currency]
                    fx_impact = asset.value * (rate_change_bps / Decimal('10000'))
                
                # Calculate market impact
                market_impact = asset.value * (scenario.market_movement_bps / Decimal('10000'))
                
                # Calculate volatility impact
                volatility_impact = asset.value * (scenario.volatility_change_bps / Decimal('10000'))
                
                row = [
                    result.run_id,
                    result.timestamp,
                    result.portfolio_id or '',
                    result.scenario_id or '',
                    asset.id,
                    asset.currency,
                    str(asset.value),
                    str(adjusted_value),
                    str(value_change),
                    str(value_change_percent),
                    str(fx_impact),
                    str(market_impact),
                    str(volatility_impact)
                ]
                writer.writerow(row)

