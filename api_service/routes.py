"""
API route handlers for risk evaluation endpoints.
"""

from flask import Blueprint, request, jsonify, send_file
from typing import Dict, Any, List
from pathlib import Path
import io
import csv

from api_service.serializers import (
    EvaluationRequest,
    EvaluationResponse,
    BatchEvaluationRequest,
    RunListResponse
)
from api_service.database import (
    save_evaluation_run,
    get_evaluation_run,
    list_evaluation_runs,
    get_run_csv_data
)
from risk_core.models import Portfolio, Scenario, Asset
from risk_core.portfolio import PortfolioManager
from risk_core.scenario import ScenarioApplicator
from risk_core.currency import CurrencyConverter
from risk_core.calculations import calculate_value_change_percent
from batch_processor.processor import BatchProcessor
from batch_processor.csv_writer import CSVWriter
import uuid
from datetime import datetime
from decimal import Decimal


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/evaluate', methods=['POST'])
def evaluate():
    """
    Evaluate a portfolio against a scenario.
    
    POST /api/v1/evaluate
    """
    try:
        # Parse and validate request
        request_data = request.get_json()
        eval_request = EvaluationRequest(**request_data)
        
        # Convert to domain models
        portfolio = _parse_portfolio(eval_request.portfolio)
        scenario = _parse_scenario(eval_request.scenario)
        
        # Perform evaluation
        base_currency = eval_request.options.get('base_currency', 'USD')
        result = _evaluate_portfolio_scenario(portfolio, scenario, base_currency)
        
        # Save to database
        run_id = save_evaluation_run(result, portfolio, scenario, base_currency)
        
        # Generate CSV
        csv_path = _generate_csv(result, portfolio, scenario)
        
        # Build response
        response = EvaluationResponse(
            run_id=run_id,
            timestamp=result.timestamp,
            result=_format_result(result),
            csv_download_url=f"/api/v1/runs/{run_id}/csv"
        )
        
        return jsonify(response.dict()), 200
        
    except ValueError as e:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": str(e)}}), 400
    except Exception as e:
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": str(e)}}), 500


@api_bp.route('/batch/evaluate', methods=['POST'])
def batch_evaluate():
    """
    Evaluate a portfolio against multiple scenarios.
    
    POST /api/v1/batch/evaluate
    """
    try:
        request_data = request.get_json()
        batch_request = BatchEvaluationRequest(**request_data)
        
        portfolio = _parse_portfolio(batch_request.portfolio)
        base_currency = batch_request.options.get('base_currency', 'USD')
        
        results = []
        for scenario_data in batch_request.scenarios:
            scenario = _parse_scenario(scenario_data)
            result = _evaluate_portfolio_scenario(portfolio, scenario, base_currency)
            run_id = save_evaluation_run(result, portfolio, scenario, base_currency)
            results.append({
                "run_id": run_id,
                "scenario_id": scenario.scenario_id,
                "result": _format_result(result)
            })
        
        return jsonify({"results": results}), 200
        
    except ValueError as e:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": str(e)}}), 400
    except Exception as e:
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": str(e)}}), 500


@api_bp.route('/runs/<run_id>', methods=['GET'])
def get_run(run_id: str):
    """
    Retrieve a specific evaluation run.
    
    GET /api/v1/runs/{run_id}
    """
    try:
        run_data = get_evaluation_run(run_id)
        if not run_data:
            return jsonify({"error": {"code": "NOT_FOUND", "message": f"Run {run_id} not found"}}), 404
        
        return jsonify(run_data), 200
        
    except Exception as e:
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": str(e)}}), 500


@api_bp.route('/runs/<run_id>/csv', methods=['GET'])
def download_run_csv(run_id: str):
    """
    Download CSV file for a specific run.
    
    GET /api/v1/runs/{run_id}/csv
    """
    try:
        csv_data = get_run_csv_data(run_id)
        if not csv_data:
            return jsonify({"error": {"code": "NOT_FOUND", "message": f"Run {run_id} not found"}}), 404
        
        # Create in-memory CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(csv_data['headers'])
        writer.writerows(csv_data['rows'])
        
        # Return as file download
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"run_{run_id}.csv"
        )
        
    except Exception as e:
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": str(e)}}), 500


@api_bp.route('/runs', methods=['GET'])
def list_runs():
    """
    List all runs with pagination.
    
    GET /api/v1/runs?page=1&limit=10&start_date=...&end_date=...&portfolio_id=...
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        portfolio_id = request.args.get('portfolio_id')
        
        runs, total = list_evaluation_runs(
            page=page,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            portfolio_id=portfolio_id
        )
        
        response = RunListResponse(
            runs=runs,
            total=total,
            page=page,
            limit=limit
        )
        
        return jsonify(response.dict()), 200
        
    except Exception as e:
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": str(e)}}), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


def register_routes(app):
    """Register all API routes with the Flask app."""
    app.register_blueprint(api_bp)


# Helper functions

def _parse_portfolio(portfolio_data: Dict[str, Any]) -> Portfolio:
    """Parse portfolio from request data."""
    assets = []
    for asset_data in portfolio_data['assets']:
        asset = Asset(
            id=asset_data['id'],
            currency=asset_data['currency'],
            value=Decimal(str(asset_data['value']))
        )
        assets.append(asset)
    
    return Portfolio(
        assets=assets,
        portfolio_id=portfolio_data.get('portfolio_id')
    )


def _parse_scenario(scenario_data: Dict[str, Any]) -> Scenario:
    """Parse scenario from request data."""
    currency_rate_changes = {}
    for currency, rate_change in scenario_data.get('currency_rate_changes', {}).items():
        currency_rate_changes[currency] = Decimal(str(rate_change))
    
    return Scenario(
        market_movement_bps=Decimal(str(scenario_data['market_movement_bps'])),
        volatility_change_bps=Decimal(str(scenario_data['volatility_change_bps'])),
        currency_rate_changes=currency_rate_changes,
        interest_rate_change_bps=Decimal(str(scenario_data['interest_rate_change_bps'])),
        scenario_id=scenario_data.get('scenario_id'),
        scenario_name=scenario_data.get('scenario_name')
    )


def _evaluate_portfolio_scenario(
    portfolio: Portfolio,
    scenario: Scenario,
    base_currency: str
) -> 'PortfolioResult':
    """Evaluate portfolio against scenario."""
    # This would use the same logic as BatchProcessor
    # For now, simplified version
    from risk_core.models import PortfolioResult
    
    run_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Calculate base value
    portfolio_manager = PortfolioManager(portfolio)
    base_breakdown = portfolio_manager.currency_breakdown()
    
    currency_converter = CurrencyConverter()
    base_portfolio_value = Decimal('0')
    for currency, value in base_breakdown.items():
        if currency == base_currency:
            base_portfolio_value += value
        else:
            converted = currency_converter.convert(value, currency, base_currency)
            base_portfolio_value += converted
    
    # Apply scenario
    scenario_applicator = ScenarioApplicator(scenario)
    adjusted_values = scenario_applicator.apply_to_portfolio(portfolio, base_currency)
    
    adjusted_portfolio_value = sum(adjusted_values.values())
    value_change = adjusted_portfolio_value - base_portfolio_value
    value_change_percent = calculate_value_change_percent(
        base_portfolio_value, adjusted_portfolio_value
    )
    
    # Currency breakdown
    currency_breakdown = {}
    for asset in portfolio.assets:
        if asset.currency not in currency_breakdown:
            currency_breakdown[asset.currency] = {
                'base_value': Decimal('0'),
                'adjusted_value': Decimal('0')
            }
        currency_breakdown[asset.currency]['base_value'] += asset.value
        currency_breakdown[asset.currency]['adjusted_value'] += adjusted_values[asset.id]
    
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
        risk_metrics=None
    )


def _format_result(result: 'PortfolioResult') -> Dict[str, Any]:
    """Format PortfolioResult for JSON response."""
    return {
        "base_portfolio_value": str(result.base_portfolio_value),
        "adjusted_portfolio_value": str(result.adjusted_portfolio_value),
        "value_change": str(result.value_change),
        "value_change_percent": str(result.value_change_percent),
        "currency_breakdown": {
            k: {kk: str(vv) for kk, vv in v.items()}
            for k, v in result.currency_breakdown.items()
        }
    }


def _generate_csv(result: 'PortfolioResult', portfolio: Portfolio, scenario: Scenario) -> Path:
    """Generate CSV file for a run."""
    # TODO: Implement CSV generation
    # This would use CSVWriter from batch_processor
    pass

