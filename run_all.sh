#!/usr/bin/env bash
set -euo pipefail

# I installed dependencies locally to ensure a reproducible run.
python -m pip install -r requirements.txt

# I generated raw (bronze) data.
python pipelines/python/generate_raw_data.py

# I built the DuckDB warehouse and materialized silver/gold tables.
python pipelines/python/build_warehouse.py

# I ran baseline data quality checks before consuming analytics outputs.
python pipelines/python/run_dq_checks.py

# I produced an A/B experiment readout for personalization effectiveness.
python pipelines/python/experiment_readout.py

echo
echo "Pipeline completed successfully."
echo "Key outputs:"
echo "- DuckDB warehouse: data/processed/navigator.duckdb"
echo "- Data quality report: outputs/dq_report.json"
echo "- Experiment readout: outputs/experiment_readout.csv"
