# Database Schema SQL Files

This directory contains SQL schema files for the Financial Risk Evaluation System database.

## Files

- **schema.sql** - Complete schema for MySQL/MariaDB (all tables in one file)
- **01_evaluation_runs.sql** - Evaluation runs table (Table 7.1)
- **02_evaluation_run_details.sql** - Run details table (Table 7.2)
- **03_scenario_parameters.sql** - Scenario parameters table (Table 7.3)
- **schema_postgresql.sql** - PostgreSQL-specific schema with JSONB and SERIAL types
- **drop_tables.sql** - Script to drop all tables (for cleanup/testing)

## Database Setup

### MySQL/MariaDB

```bash
mysql -u username -p database_name < sql/schema.sql
```

Or run individual files:
```bash
mysql -u username -p database_name < sql/01_evaluation_runs.sql
mysql -u username -p database_name < sql/02_evaluation_run_details.sql
mysql -u username -p database_name < sql/03_scenario_parameters.sql
```

### PostgreSQL

```bash
psql -U username -d database_name -f sql/schema_postgresql.sql
```

## Table Descriptions

### evaluation_runs
Stores summary information for each evaluation run, including portfolio and scenario identifiers, base and adjusted values, and calculated changes.

### evaluation_run_details
Stores asset-level results for each evaluation run, including individual asset impacts from market movements, volatility changes, and currency rate changes.

### scenario_parameters
Stores the scenario parameters used for each run, providing an audit trail for reproducibility. Uses JSON/JSONB to store currency rate changes as a key-value mapping.

## Differences Between MySQL and PostgreSQL

1. **Auto-increment**: MySQL uses `AUTO_INCREMENT`, PostgreSQL uses `SERIAL` or `BIGSERIAL`
2. **JSON**: MySQL uses `JSON`, PostgreSQL uses `JSONB` (recommended for better performance)
3. **Index creation**: MySQL allows inline index creation, PostgreSQL requires separate `CREATE INDEX` statements

## Notes

- All monetary values use `DECIMAL(18, 2)` for precision
- Percentage values use `DECIMAL(10, 4)` to support basis points precision
- Foreign keys use `ON DELETE CASCADE` to maintain referential integrity
- Indexes are created on frequently queried columns (timestamp, portfolio_id, run_id, asset_id)

