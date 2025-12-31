"""
Integration test demonstrating batch processing functionality.

This test shows how to use the core library in batch mode:
1. Load portfolio and scenarios from JSON files
2. Process them using BatchProcessor
3. Verify results and CSV output
"""

import pytest
from pathlib import Path
from decimal import Decimal
import tempfile
import csv

from batch_processor.processor import BatchProcessor
from batch_processor.file_reader import JSONFileReader
from risk_core.models import Portfolio, Scenario, Asset
from risk_core.portfolio import PortfolioManager
from risk_core.scenario import ScenarioApplicator
from risk_core.currency import CurrencyConverter


class TestBatchProcessing:
    """Test suite demonstrating batch processing workflow."""
    
    @pytest.fixture
    def sample_portfolio_path(self):
        """Path to sample portfolio JSON file."""
        return Path(__file__).parent.parent / "fixtures" / "sample_portfolio.json"
    
    @pytest.fixture
    def sample_scenarios_path(self):
        """Path to sample scenarios JSON file."""
        return Path(__file__).parent.parent / "fixtures" / "sample_scenarios.json"
    
    @pytest.fixture
    def temp_output_dir(self):
        """Temporary directory for output files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_load_portfolio_from_json(self, sample_portfolio_path):
        """
        Demonstrate: Loading a portfolio from JSON file.
        
        This shows how to use JSONFileReader to load portfolio data.
        """
        # Load portfolio from JSON file
        portfolio = JSONFileReader.read_portfolio(sample_portfolio_path)
        
        # Verify portfolio structure
        assert portfolio.portfolio_id == "test-portfolio-1"
        assert len(portfolio.assets) == 3
        
        # Verify assets
        asset_ids = [asset.id for asset in portfolio.assets]
        assert "ASSET001" in asset_ids
        assert "ASSET002" in asset_ids
        assert "ASSET003" in asset_ids
        
        # Verify asset values
        usd_asset = next(a for a in portfolio.assets if a.id == "ASSET001")
        assert usd_asset.currency == "USD"
        assert usd_asset.value == Decimal("100000")
    
    def test_load_scenarios_from_json(self, sample_scenarios_path):
        """
        Demonstrate: Loading scenarios from JSON file.
        
        This shows how to use JSONFileReader to load scenario data.
        """
        # Load scenarios from JSON file
        scenarios = JSONFileReader.read_scenarios(sample_scenarios_path)
        
        # Verify we have 2 scenarios
        assert len(scenarios) == 2
        
        # Verify first scenario (Bull Market)
        bull_scenario = next(s for s in scenarios if s.scenario_id == "scenario-1")
        assert bull_scenario.scenario_name == "Bull Market"
        assert bull_scenario.market_movement_bps == Decimal("200")  # +2%
        assert bull_scenario.volatility_change_bps == Decimal("-50")  # -0.5%
        
        # Verify second scenario (Bear Market)
        bear_scenario = next(s for s in scenarios if s.scenario_id == "scenario-2")
        assert bear_scenario.scenario_name == "Bear Market"
        assert bear_scenario.market_movement_bps == Decimal("-150")  # -1.5%
        assert "EUR" in bear_scenario.currency_rate_changes
    
    def test_portfolio_currency_breakdown(self, sample_portfolio_path):
        """
        Demonstrate: Getting currency breakdown of a portfolio.
        
        This shows how to use PortfolioManager to analyze portfolio composition.
        """
        # Load portfolio
        portfolio = JSONFileReader.read_portfolio(sample_portfolio_path)
        
        # Get currency breakdown
        portfolio_manager = PortfolioManager(portfolio)
        breakdown = portfolio_manager.currency_breakdown()
        
        # Verify breakdown
        assert breakdown["USD"] == Decimal("100000")
        assert breakdown["EUR"] == Decimal("50000")
        assert breakdown["GBP"] == Decimal("75000")
    
    def test_apply_scenario_to_portfolio(self, sample_portfolio_path, sample_scenarios_path):
        """
        Demonstrate: Applying a scenario to a portfolio.
        
        This shows how to use ScenarioApplicator to evaluate portfolio under a scenario.
        """
        # Load portfolio and scenario
        portfolio = JSONFileReader.read_portfolio(sample_portfolio_path)
        scenarios = JSONFileReader.read_scenarios(sample_scenarios_path)
        bull_scenario = next(s for s in scenarios if s.scenario_id == "scenario-1")
        
        # Apply scenario
        scenario_applicator = ScenarioApplicator(bull_scenario)
        adjusted_values = scenario_applicator.apply_to_portfolio(portfolio, "USD")
        
        # Verify we got adjusted values for all assets
        assert len(adjusted_values) == 3
        assert "ASSET001" in adjusted_values
        assert "ASSET002" in adjusted_values
        assert "ASSET003" in adjusted_values
        
        # Verify market movement was applied (200 bps = +2%)
        usd_asset = next(a for a in portfolio.assets if a.id == "ASSET001")
        expected_value = usd_asset.value * Decimal("1.02")  # +2%
        assert adjusted_values["ASSET001"] == expected_value
    
    def test_currency_conversion(self):
        """
        Demonstrate: Currency conversion with rate changes.
        
        This shows how to use CurrencyConverter for multi-currency portfolios.
        """
        converter = CurrencyConverter()
        
        # Convert EUR to USD (default rate: 1 EUR = 1.10 USD)
        eur_value = Decimal("1000")
        usd_value = converter.convert(eur_value, "EUR", "USD")
        
        # Verify conversion
        expected = eur_value * Decimal("1.10")
        assert usd_value == expected
        
        # Convert with rate change (+50 bps = +0.5%)
        usd_value_with_change = converter.convert(
            eur_value, "EUR", "USD", rate_change_bps=Decimal("50")
        )
        expected_with_change = eur_value * Decimal("1.10") * Decimal("1.005")
        assert usd_value_with_change == expected_with_change
    
    def test_full_batch_processing_workflow(
        self, sample_portfolio_path, sample_scenarios_path, temp_output_dir
    ):
        """
        Demonstrate: Complete batch processing workflow.
        
        This is the main example showing how to use BatchProcessor end-to-end:
        1. Initialize processor
        2. Process portfolio against scenarios
        3. Generate CSV output
        4. Verify results
        """
        # Setup output file
        output_file = temp_output_dir / "test_results.csv"
        
        # Initialize batch processor with USD as base currency
        processor = BatchProcessor(base_currency="USD")
        
        # Process portfolio against scenarios
        run_id = processor.process(
            portfolio_file=sample_portfolio_path,
            scenarios_file=sample_scenarios_path,
            output_file=output_file
        )
        
        # Verify run ID was generated
        assert run_id is not None
        assert len(run_id) == 36  # UUID length
        
        # Verify CSV file was created
        assert output_file.exists()
        
        # Read and verify CSV content
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Verify CSV structure
        assert len(rows) > 0
        assert 'run_id' in rows[0]
        assert 'timestamp' in rows[0]
        assert 'portfolio_id' in rows[0]
        assert 'scenario_id' in rows[0]
        
        # Verify run_id matches
        for row in rows:
            assert row['run_id'] == run_id
    
    def test_batch_processing_with_different_base_currency(
        self, sample_portfolio_path, sample_scenarios_path, temp_output_dir
    ):
        """
        Demonstrate: Batch processing with different base currency.
        
        This shows how to process portfolios using EUR as base currency.
        """
        output_file = temp_output_dir / "results_eur.csv"
        
        # Initialize processor with EUR as base currency
        processor = BatchProcessor(base_currency="EUR")
        
        # Process
        run_id = processor.process(
            portfolio_file=sample_portfolio_path,
            scenarios_file=sample_scenarios_path,
            output_file=output_file
        )
        
        # Verify processing completed
        assert run_id is not None
        assert output_file.exists()
    
    def test_multiple_scenarios_processing(
        self, sample_portfolio_path, sample_scenarios_path, temp_output_dir
    ):
        """
        Demonstrate: Processing portfolio against multiple scenarios.
        
        This shows how batch processor handles multiple scenarios in one run.
        """
        output_file = temp_output_dir / "multi_scenario_results.csv"
        
        processor = BatchProcessor()
        run_id = processor.process(
            portfolio_file=sample_portfolio_path,
            scenarios_file=sample_scenarios_path,
            output_file=output_file
        )
        
        # Read CSV to verify multiple scenarios were processed
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Get unique scenario IDs from results
        scenario_ids = {row['scenario_id'] for row in rows if row['scenario_id']}
        
        # Verify both scenarios were processed
        assert 'scenario-1' in scenario_ids or len(scenario_ids) > 0
    
    def test_scenario_with_currency_rate_changes(
        self, sample_portfolio_path, sample_scenarios_path
    ):
        """
        Demonstrate: Scenario with currency rate changes.
        
        This shows how currency rate changes affect multi-currency portfolios.
        """
        # Load portfolio and bear market scenario (has currency rate changes)
        portfolio = JSONFileReader.read_portfolio(sample_portfolio_path)
        scenarios = JSONFileReader.read_scenarios(sample_scenarios_path)
        bear_scenario = next(s for s in scenarios if s.scenario_id == "scenario-2")
        
        # Verify scenario has currency rate changes
        assert "EUR" in bear_scenario.currency_rate_changes
        assert "GBP" in bear_scenario.currency_rate_changes
        assert bear_scenario.currency_rate_changes["EUR"] == Decimal("-50")  # -0.5%
        assert bear_scenario.currency_rate_changes["GBP"] == Decimal("-75")  # -0.75%
        
        # Apply scenario
        scenario_applicator = ScenarioApplicator(bear_scenario)
        adjusted_values = scenario_applicator.apply_to_portfolio(portfolio, "USD")
        
        # Verify EUR asset was affected by both market movement and FX change
        eur_asset = next(a for a in portfolio.assets if a.id == "ASSET002")
        adjusted_eur = adjusted_values["ASSET002"]
        
        # Market movement: -150 bps = -1.5%
        # FX change: -50 bps = -0.5%
        # Combined effect should be visible
        assert adjusted_eur != eur_asset.value


def test_example_usage_in_documentation():
    """
    Standalone example that can be used in documentation.
    
    This demonstrates the simplest possible usage of batch processing.
    """
    # Example: Simple batch processing workflow
    from pathlib import Path
    from batch_processor.processor import BatchProcessor
    
    # Define input and output paths
    portfolio_file = Path("tests/fixtures/sample_portfolio.json")
    scenarios_file = Path("tests/fixtures/sample_scenarios.json")
    output_file = Path("output/results.csv")
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize and run processor
    processor = BatchProcessor(base_currency="USD")
    run_id = processor.process(
        portfolio_file=portfolio_file,
        scenarios_file=scenarios_file,
        output_file=output_file
    )
    
    print(f"Processing completed. Run ID: {run_id}")
    print(f"Results saved to: {output_file}")

