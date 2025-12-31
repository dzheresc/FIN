-- Financial Risk Evaluation System - Complete Database Schema
-- Supports MySQL/MariaDB and PostgreSQL (with minor adjustments)

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_portfolio_id (portfolio_id)
);

-- Table 7.2: Run Details (for asset-level results)
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
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    INDEX idx_run_id (run_id),
    INDEX idx_asset_id (asset_id)
);

-- Table 7.3: Scenario Parameters (for audit trail)
CREATE TABLE scenario_parameters (
    run_id VARCHAR(36) PRIMARY KEY,
    market_movement_bps DECIMAL(10, 2),
    volatility_change_bps DECIMAL(10, 2),
    interest_rate_change_bps DECIMAL(10, 2),
    currency_rate_changes JSON,
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id) ON DELETE CASCADE
);

