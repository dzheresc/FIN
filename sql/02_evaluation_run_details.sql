-- Table 7.2: Evaluation Run Details
-- Stores asset-level results for each evaluation run

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

-- Comments for documentation
-- id: Auto-incrementing primary key
-- run_id: Foreign key to evaluation_runs table
-- asset_id: Identifier for the asset
-- currency: Currency of the asset (ISO 4217 code)
-- base_value: Original value of the asset before scenario application
-- adjusted_value: Value of the asset after scenario application
-- value_change: Absolute change in asset value
-- value_change_percent: Percentage change in asset value
-- fx_impact: Impact from currency rate changes (in base currency)
-- market_impact: Impact from market movement (in base currency)
-- volatility_impact: Impact from volatility changes (in base currency)

