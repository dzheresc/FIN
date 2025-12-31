-- Table 7.3: Scenario Parameters
-- Stores scenario parameters for audit trail and reproducibility

CREATE TABLE scenario_parameters (
    run_id VARCHAR(36) PRIMARY KEY,
    market_movement_bps DECIMAL(10, 2),
    volatility_change_bps DECIMAL(10, 2),
    interest_rate_change_bps DECIMAL(10, 2),
    currency_rate_changes JSON,
    FOREIGN KEY (run_id) REFERENCES evaluation_runs(run_id) ON DELETE CASCADE
);

-- Comments for documentation
-- run_id: Foreign key to evaluation_runs table (one-to-one relationship)
-- market_movement_bps: Market movement in basis points (e.g., 100 = 1%)
-- volatility_change_bps: Volatility change in basis points
-- interest_rate_change_bps: Interest rate change in basis points
-- currency_rate_changes: JSON object mapping currency codes to rate changes in BPS
--   Example: {"USD": 50, "EUR": -25, "GBP": 100}

-- Note: For PostgreSQL, use JSONB instead of JSON for better performance
-- For SQLite, use TEXT and store as JSON string

