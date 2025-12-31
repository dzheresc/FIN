-- Drop all tables in reverse order of dependencies
-- Use this script to clean up the database schema

-- Drop tables (order matters due to foreign key constraints)
DROP TABLE IF EXISTS scenario_parameters;
DROP TABLE IF EXISTS evaluation_run_details;
DROP TABLE IF EXISTS evaluation_runs;

-- Note: For PostgreSQL, you may need to drop indexes first if they have dependencies
-- DROP INDEX IF EXISTS idx_currency_rate_changes;
-- DROP INDEX IF EXISTS idx_asset_id;
-- DROP INDEX IF EXISTS idx_run_id;
-- DROP INDEX IF EXISTS idx_portfolio_id;
-- DROP INDEX IF EXISTS idx_timestamp;

