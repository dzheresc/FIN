"""
Example script demonstrating batch processing usage.

This example demonstrates how to use the batch processing functionality
to evaluate a portfolio against multiple scenarios.

Run this script from the project root:
    python examples/batch_processing_example.py
"""

from pathlib import Path
from batch_processor.processor import BatchProcessor
from batch_processor.file_reader import JSONFileReader
from risk_core.models import Portfolio, Scenario
from risk_core.portfolio import PortfolioManager
from risk_core.scenario import ScenarioApplicator
from decimal import Decimal


def main():
    """Main example function."""
    print("=" * 60)
    print("Financial Risk Evaluation System - Batch Processing Example")
    print("=" * 60)
    print()
    
    # Step 1: Load portfolio from JSON file
    print("Step 1: Loading portfolio from JSON file...")
    portfolio_file = Path("tests/fixtures/sample_portfolio.json")
    portfolio = JSONFileReader.read_portfolio(portfolio_file)
    print(f"  ✓ Loaded portfolio: {portfolio.portfolio_id}")
    print(f"  ✓ Number of assets: {len(portfolio.assets)}")
    
    # Display portfolio composition
    portfolio_manager = PortfolioManager(portfolio)
    breakdown = portfolio_manager.currency_breakdown()
    print("  Portfolio composition:")
    for currency, value in breakdown.items():
        print(f"    - {currency}: {value:,.2f}")
    print()
    
    # Step 2: Load scenarios from JSON file
    print("Step 2: Loading scenarios from JSON file...")
    scenarios_file = Path("tests/fixtures/sample_scenarios.json")
    scenarios = JSONFileReader.read_scenarios(scenarios_file)
    print(f"  ✓ Loaded {len(scenarios)} scenario(s)")
    for scenario in scenarios:
        print(f"    - {scenario.scenario_id}: {scenario.scenario_name}")
    print()
    
    # Step 3: Demonstrate scenario application (manual)
    print("Step 3: Applying scenario manually (for demonstration)...")
    if scenarios:
        scenario = scenarios[0]
        print(f"  Applying scenario: {scenario.scenario_name}")
        print(f"    Market movement: {scenario.market_movement_bps} bps ({scenario.market_movement_bps / 100:.2f}%)")
        print(f"    Volatility change: {scenario.volatility_change_bps} bps")
        
        scenario_applicator = ScenarioApplicator(scenario)
        adjusted_values = scenario_applicator.apply_to_portfolio(portfolio, "USD")
        
        print("  Asset adjustments:")
        for asset in portfolio.assets:
            base_value = asset.value
            adjusted_value = adjusted_values[asset.id]
            change = adjusted_value - base_value
            change_pct = (change / base_value * 100) if base_value > 0 else 0
            print(f"    {asset.id} ({asset.currency}): "
                  f"{base_value:,.2f} → {adjusted_value:,.2f} "
                  f"({change:+,.2f}, {change_pct:+.2f}%)")
    print()
    
    # Step 4: Full batch processing
    print("Step 4: Running full batch processing...")
    output_file = Path("output/example_results.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    processor = BatchProcessor(base_currency="USD")
    run_id = processor.process(
        portfolio_file=portfolio_file,
        scenarios_file=scenarios_file,
        output_file=output_file
    )
    
    print(f"  ✓ Processing completed")
    print(f"  ✓ Run ID: {run_id}")
    print(f"  ✓ Results saved to: {output_file}")
    print()
    
    # Step 5: Display summary
    print("Step 5: Reading results from CSV...")
    import csv
    if output_file.exists():
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"  ✓ Found {len(rows)} result row(s)")
        if rows:
            print("  Sample result:")
            sample = rows[0]
            for key, value in sample.items():
                if value:  # Only show non-empty values
                    print(f"    {key}: {value}")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

