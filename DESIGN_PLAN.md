# Financial Risk Evaluation System - Design Plan

## 1. System Overview

A financial risk evaluation system that processes asset portfolios against market scenarios to calculate risk metrics. The system supports batch processing and real-time REST API access, with results stored in CSV files and a database.

## 2. Architecture Components

### 2.1 Core Library (`risk_core`)
- **Purpose**: Pure business logic for risk calculations
- **Dependencies**: Minimal (only standard libraries for calculations)
- **Responsibilities**:
  - Asset portfolio modeling
  - Scenario application
  - Risk metric calculations
  - Currency conversion
  - Interest rate adjustments

### 2.2 Batch Processing Module (`batch_processor`)
- **Purpose**: Process JSON input files and generate CSV outputs
- **Dependencies**: Core library, file I/O libraries
- **Responsibilities**:
  - Read JSON input files
  - Validate input data
  - Execute risk calculations
  - Generate CSV output files
  - Log processing metadata

### 2.3 REST API Service (`api_service`)
- **Purpose**: HTTP interface for real-time risk evaluation
- **Dependencies**: Core library, web framework, database client
- **Responsibilities**:
  - Accept HTTP requests with portfolio and scenario data
  - Execute risk calculations
  - Return JSON responses
  - Store results in database
  - Generate CSV files on demand

### 2.4 Data Storage Layer (`storage`)
- **Purpose**: Persist all evaluation runs
- **Dependencies**: Database client library
- **Responsibilities**:
  - Store run metadata (timestamp, input parameters)
  - Store results in structured format
  - Query historical runs
  - Support CSV export from database

## 3. Data Models

### 3.1 Asset Model
```json
{
  "id": "string",
  "currency": "string (ISO 4217 code)",
  "value": "number (decimal)"
}
```

### 3.2 Portfolio Model
```json
{
  "portfolio_id": "string (optional)",
  "assets": [
    {
      "id": "string",
      "currency": "string",
      "value": "number"
    }
  ]
}
```

### 3.3 Scenario Model
```json
{
  "scenario_id": "string (optional)",
  "scenario_name": "string (optional)",
  "market_movement_bps": "number (basis points, e.g., 100 = 1%)",
  "volatility_change_bps": "number (basis points)",
  "currency_rate_changes": {
    "USD": 50,
    "EUR": -25,
    "GBP": 100
  },
  "interest_rate_change_bps": "number (basis points)"
}
```

### 3.4 Risk Evaluation Result Model
```json
{
  "run_id": "string (UUID)",
  "timestamp": "ISO 8601 datetime",
  "portfolio_id": "string",
  "scenario_id": "string",
  "base_portfolio_value": "number",
  "adjusted_portfolio_value": "number",
  "value_change": "number",
  "value_change_percent": "number",
  "currency_breakdown": {
    "USD": {
      "base_value": "number",
      "adjusted_value": "number",
      "fx_impact": "number"
    }
  },
  "risk_metrics": {
    "var_95": "number (optional)",
    "expected_shortfall": "number (optional)"
  }
}
```

## 4. Core Library Design (`risk_core`)

### 4.1 Module Structure
```
risk_core/
├── __init__.py
├── models.py          # Data models (Asset, Portfolio, Scenario, Result)
├── portfolio.py       # Portfolio operations
├── scenario.py        # Scenario application logic
├── calculations.py    # Risk calculation functions
├── currency.py        # Currency conversion utilities
└── validators.py      # Input validation
```

### 4.2 Key Classes and Functions

#### `Portfolio` Class
- `__init__(assets: List[Asset])`
- `total_value(base_currency: str) -> float`
- `currency_breakdown() -> Dict[str, float]`
- `apply_scenario(scenario: Scenario) -> PortfolioResult`

#### `Scenario` Class
- `__init__(market_movement_bps, volatility_change_bps, currency_rate_changes, interest_rate_change_bps)`
- `apply_to_asset(asset: Asset) -> float`
- `apply_to_portfolio(portfolio: Portfolio) -> PortfolioResult`

#### `CurrencyConverter` Class
- `convert(value: float, from_currency: str, to_currency: str, rate_change_bps: float) -> float`
- `get_base_rates() -> Dict[str, float]`

#### Calculation Functions
- `calculate_portfolio_var(portfolio: Portfolio, scenario: Scenario, confidence: float) -> float`
- `calculate_expected_shortfall(portfolio: Portfolio, scenario: Scenario) -> float`
- `apply_market_movement(value: float, movement_bps: float) -> float`
- `apply_volatility_adjustment(value: float, volatility_change_bps: float) -> float`

### 4.3 Calculation Logic

1. **Market Movement Application**:
   - `adjusted_value = base_value * (1 + market_movement_bps / 10000)`

2. **Volatility Adjustment**:
   - Apply volatility scaling factor to value
   - `volatility_factor = 1 + (volatility_change_bps / 10000) * volatility_multiplier`

3. **Currency Rate Changes**:
   - Convert all assets to base currency (e.g., USD)
   - Apply FX rate changes: `new_rate = base_rate * (1 + rate_change_bps / 10000)`
   - Recalculate portfolio value in base currency

4. **Interest Rate Impact**:
   - Apply duration/convexity adjustments if applicable
   - For stocks: indirect impact through discount rate changes

## 5. Batch Processing Design (`batch_processor`)

### 5.1 Module Structure
```
batch_processor/
├── __init__.py
├── file_reader.py     # JSON input parsing
├── processor.py       # Main batch processing logic
├── csv_writer.py     # CSV output generation
└── logger.py         # Processing logs
```

### 5.2 Processing Workflow

1. **Input Validation**
   - Validate JSON schema
   - Check required fields
   - Validate currency codes
   - Validate numeric ranges

2. **Portfolio Loading**
   - Parse portfolio JSON
   - Create Portfolio object
   - Validate asset data

3. **Scenario Application**
   - Load scenario(s) from input
   - Apply each scenario to portfolio
   - Generate results

4. **Output Generation**
   - Create CSV file with results
   - Include metadata (timestamp, run_id)
   - Format: columns for asset_id, currency, base_value, adjusted_value, change, etc.

### 5.3 CSV Output Format

```csv
run_id,timestamp,portfolio_id,scenario_id,asset_id,currency,base_value,adjusted_value,value_change,value_change_percent,fx_impact,market_impact,volatility_impact
uuid-123,2024-01-15T10:30:00Z,portfolio-1,scenario-1,ASSET001,USD,100000,105000,5000,5.0,0,5000,0
uuid-123,2024-01-15T10:30:00Z,portfolio-1,scenario-1,ASSET002,EUR,50000,51250,1250,2.5,1250,0,0
```

### 5.4 Command-Line Interface

```bash
python -m batch_processor \
  --portfolio portfolio.json \
  --scenarios scenarios.json \
  --output results.csv \
  --base-currency USD
```

## 6. REST API Design (`api_service`)

### 6.1 API Endpoints

#### POST `/api/v1/evaluate`
Evaluate a portfolio against a scenario

**Request Body**:
```json
{
  "portfolio": {
    "assets": [...]
  },
  "scenario": {
    "market_movement_bps": 100,
    "volatility_change_bps": 50,
    "currency_rate_changes": {...},
    "interest_rate_change_bps": 25
  },
  "options": {
    "base_currency": "USD",
    "include_metrics": ["var", "expected_shortfall"]
  }
}
```

**Response**:
```json
{
  "run_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z",
  "result": {
    "base_portfolio_value": 150000,
    "adjusted_portfolio_value": 156250,
    "value_change": 6250,
    "value_change_percent": 4.17,
    ...
  },
  "csv_download_url": "/api/v1/runs/{run_id}/csv"
}
```

#### GET `/api/v1/runs/{run_id}`
Retrieve a specific evaluation run

#### GET `/api/v1/runs/{run_id}/csv`
Download CSV file for a specific run

#### GET `/api/v1/runs`
List all runs with pagination
- Query params: `page`, `limit`, `start_date`, `end_date`, `portfolio_id`

#### POST `/api/v1/batch/evaluate`
Batch evaluation (multiple scenarios)
- Accepts array of scenarios
- Returns array of results

### 6.2 API Service Structure
```
api_service/
├── __init__.py
├── app.py             # Flask/FastAPI application
├── routes.py          # API route handlers
├── database.py        # Database operations
├── serializers.py     # Request/response serialization
└── config.py          # Configuration
```

## 7. Database Schema Design

### 7.1 Runs Table
```sql
CREATE TABLE evaluation_runs (
    run_id VARCHAR(36) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    portfolio_id VARCHAR(255),
    scenario_id VARCHAR(255),
    base_portfolio_value DECIMAL(18, 2),
    adjusted_portfolio_value DECIMAL(18, 2),
    value_change DECIMAL(18, 2),
    value_change_percent DECIMAL(10, 4),
    base_currency VARCHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_portfolio_id (portfolio_id)
);
```

### 7.2 Run Details Table (for asset-level results)
```sql
CREATE TABLE evaluation_run_details (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    run_id VARCHAR(36) NOT NULL,
    asset_id VARCHAR(255) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    base_value DECIMAL(18, 2),
    adjusted_value DECIMAL(18, 2),
    value_change DECIMAL(18, 2),
    value_change_percent DECIMAL(10, 4),
    fx_impact DECIMAL(18, 2),
    market_impact DECIMAL(18, 2),
    volatility_impact DECIMAL(18, 2),
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id),
    INDEX idx_run_id (run_id),
    INDEX idx_asset_id (asset_id)
);
```

### 7.3 Scenario Parameters Table (optional, for audit)
```sql
CREATE TABLE scenario_parameters (
    run_id VARCHAR(36) PRIMARY KEY,
    market_movement_bps DECIMAL(10, 2),
    volatility_change_bps DECIMAL(10, 2),
    interest_rate_change_bps DECIMAL(10, 2),
    currency_rate_changes JSON,
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id)
);
```

## 8. Technology Stack Recommendations

### 8.1 Core Library
- **Language**: Python 3.9+
- **Dependencies**: 
  - `pydantic` for data validation
  - `decimal` for precise financial calculations

### 8.2 Batch Processor
- **Language**: Python 3.9+
- **Dependencies**:
  - Core library
  - `jsonschema` for JSON validation
  - `pandas` (optional) for CSV operations

### 8.3 REST API
- **Framework**: FastAPI or Flask
- **Database**: PostgreSQL or MySQL
- **ORM**: SQLAlchemy or similar
- **Dependencies**:
  - Core library
  - Database client
  - Web framework

## 9. Error Handling

### 9.1 Validation Errors
- Invalid currency codes
- Negative values where not allowed
- Missing required fields
- Invalid basis points ranges

### 9.2 Processing Errors
- Currency conversion failures
- Calculation overflow/underflow
- Database connection failures

### 9.3 Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid currency code: XXX",
    "field": "assets[0].currency"
  }
}
```

## 10. Configuration

### 10.1 Configuration Files
- `config.yaml` or environment variables
- Database connection settings
- Base currency rates (or API endpoint)
- Default calculation parameters
- Logging configuration

## 11. Testing Strategy

### 11.1 Unit Tests
- Core calculation functions
- Currency conversion
- Scenario application logic

### 11.2 Integration Tests
- Batch processing end-to-end
- API endpoints
- Database operations

### 11.3 Test Data
- Sample portfolios
- Standard scenarios
- Edge cases (zero values, extreme BPS changes)

## 12. Future Enhancements

1. **Additional Asset Types**: Bonds, derivatives, options
2. **Advanced Risk Metrics**: VaR, CVaR, stress testing
3. **Historical Analysis**: Compare runs over time
4. **Real-time Market Data**: Integration with market data feeds
5. **Multi-currency Base**: Support for any base currency
6. **Parallel Processing**: Handle large portfolios efficiently
7. **Caching**: Cache currency rates and common calculations
8. **Authentication/Authorization**: Secure API access

## 13. File Structure Summary

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
├── requirements.txt
├── README.md
└── DESIGN_PLAN.md
```

## 14. Implementation Phases

### Phase 1: Core Library
- Implement data models
- Build portfolio and scenario classes
- Implement basic calculations
- Unit tests

### Phase 2: Batch Processor
- File I/O
- CSV generation
- CLI interface
- Integration tests

### Phase 3: Database Layer
- Schema design and creation
- ORM models
- CRUD operations
- Migration scripts

### Phase 4: REST API
- API endpoints
- Request/response handling
- Database integration
- Error handling

### Phase 5: Integration & Testing
- End-to-end testing
- Performance optimization
- Documentation
- Deployment preparation

