-- Table 7.1: Evaluation Runs
-- Stores summary information for each evaluation run

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

-- Comments for documentation
-- run_id: Unique identifier (UUID) for the evaluation run
-- timestamp: ISO 8601 timestamp when the evaluation was performed
-- portfolio_id: Optional identifier for the portfolio being evaluated
-- scenario_id: Optional identifier for the scenario applied
-- base_portfolio_value: Total portfolio value before scenario application
-- adjusted_portfolio_value: Total portfolio value after scenario application
-- value_change: Absolute change in portfolio value
-- value_change_percent: Percentage change in portfolio value
-- base_currency: Base currency used for calculations (ISO 4217 code)
-- created_at: Database record creation timestamp

