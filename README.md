# Financial Risk Evaluation System

A comprehensive system for evaluating financial portfolios against market scenarios, supporting batch processing and REST API access.

## Features

- **Portfolio Risk Evaluation**: Evaluate portfolios against market scenarios
- **Scenario Modeling**: Support for market movements, volatility changes, currency rate changes, and interest rate changes
- **Batch Processing**: Process JSON input files and generate CSV outputs
- **REST API**: Real-time evaluation via HTTP interface
- **Database Storage**: Persistent storage of all evaluation runs with timestamping
- **Multi-Currency Support**: Handle portfolios with assets in different currencies

## Project Structure

```
financial_risk_system/
├── risk_core/              # Core library
│   ├── models.py
│   ├── portfolio.py
│   ├── scenario.py
│   ├── calculations.py
│   ├── currency.py
│   └── validators.py
├── batch_processor/        # Batch processing
│   ├── file_reader.py
│   ├── processor.py
│   ├── csv_writer.py
│   └── cli.py
├── api_service/           # REST API
│   ├── app.py
│   ├── routes.py
│   ├── database.py
│   └── serializers.py
├── storage/                # Database models
│   ├── models.py
│   └── migrations/
├── tests/                  # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── config/                 # Configuration
│   └── config.yaml
├── sql/                    # Database schema
├── requirements.txt
├── README.md
└── DESIGN_PLAN.md
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
# For MySQL/MariaDB
mysql -u username -p database_name < sql/schema.sql

# For PostgreSQL
psql -U username -d database_name -f sql/schema_postgresql.sql
```

4. Configure the application:
   - Edit `config/config.yaml` with your database and application settings

## Usage

### Batch Processing

Process portfolios and scenarios from JSON files:

```bash
python -m batch_processor \
  --portfolio portfolio.json \
  --scenarios scenarios.json \
  --output results.csv \
  --base-currency USD
```

### REST API

Start the API server:

```bash
python -m api_service.app
```

The API will be available at `http://localhost:5000`

#### API Endpoints

- `POST /api/v1/evaluate` - Evaluate a portfolio against a scenario
- `POST /api/v1/batch/evaluate` - Batch evaluation with multiple scenarios
- `GET /api/v1/runs/{run_id}` - Retrieve a specific evaluation run
- `GET /api/v1/runs/{run_id}/csv` - Download CSV for a run
- `GET /api/v1/runs` - List all runs with pagination
- `GET /api/v1/health` - Health check

## Input Format

### Portfolio JSON

```json
{
  "portfolio_id": "portfolio-1",
  "assets": [
    {
      "id": "ASSET001",
      "currency": "USD",
      "value": 100000
    }
  ]
}
```

### Scenario JSON

```json
{
  "scenario_id": "scenario-1",
  "market_movement_bps": 100,
  "volatility_change_bps": 50,
  "currency_rate_changes": {
    "EUR": -25,
    "GBP": 100
  },
  "interest_rate_change_bps": 25
}
```

## Output Format

Results are stored in CSV format with the following columns:
- run_id, timestamp, portfolio_id, scenario_id
- asset_id, currency, base_value, adjusted_value
- value_change, value_change_percent
- fx_impact, market_impact, volatility_impact

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
```

## Configuration

Edit `config/config.yaml` to configure:
- Database connection settings
- API host and port
- Currency settings
- Logging configuration
- File storage paths

## License

[Add your license here]

## Documentation

See `DESIGN_PLAN.md` for detailed system design and architecture.
