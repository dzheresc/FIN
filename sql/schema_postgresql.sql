-- Financial Risk Evaluation System - PostgreSQL Database Schema
-- PostgreSQL-specific version with JSONB and SERIAL types

-- Table 7.1: Evaluation Runs
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_timestamp ON evaluation_runs(timestamp);
CREATE INDEX idx_portfolio_id ON evaluation_runs(portfolio_id);

-- Table 7.2: Run Details (for asset-level results)
CREATE TABLE evaluation_run_details (
    id BIGSERIAL PRIMARY KEY,
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
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_run_id ON evaluation_run_details(run_id);
CREATE INDEX idx_asset_id ON evaluation_run_details(asset_id);

-- Table 7.3: Scenario Parameters (for audit trail)
CREATE TABLE scenario_parameters (
    run_id VARCHAR(36) PRIMARY KEY,
    market_movement_bps DECIMAL(10, 2),
    volatility_change_bps DECIMAL(10, 2),
    interest_rate_change_bps DECIMAL(10, 2),
    currency_rate_changes JSONB,
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id) ON DELETE CASCADE
);

-- Note: JSONB is used instead of JSON for better performance and indexing capabilities
-- You can create a GIN index on currency_rate_changes if needed:
-- CREATE INDEX idx_currency_rate_changes ON scenario_parameters USING GIN (currency_rate_changes);

