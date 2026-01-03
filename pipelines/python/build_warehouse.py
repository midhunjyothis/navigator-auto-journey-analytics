"""
I built a local DuckDB warehouse from the raw parquet files and then
materialized conformed (silver) and analytics (gold) tables using the
versioned SQL definitions in pipelines/sql.

This gave me a reproducible local environment to validate the funnel,
KPIs, and experiment readouts end-to-end.
"""

from __future__ import annotations

import os
import duckdb

DB_PATH = os.environ.get("NAV_DB_PATH", "data/processed/navigator.duckdb")

RAW_EVENTS = "data/raw/raw_events.parquet"
RAW_CUSTOMERS = "data/raw/raw_customers.parquet"
RAW_VEHICLES = "data/raw/raw_vehicles.parquet"
RAW_ELIG = "data/raw/raw_eligibility_decisions.parquet"
RAW_LEADS = "data/raw/raw_leads.parquet"
RAW_PURCHASES = "data/raw/raw_purchases.parquet"


def main() -> None:
    os.makedirs("data/processed", exist_ok=True)
    con = duckdb.connect(DB_PATH)

    con.execute("create schema if not exists bronze;")
    con.execute("create schema if not exists silver;")
    con.execute("create schema if not exists gold;")

    # Loaded bronze tables directly from parquet (raw, no business logic).
    con.execute("drop table if exists bronze.raw_events;")
    con.execute(
        f"create table bronze.raw_events as select * from read_parquet('{RAW_EVENTS}');")

    con.execute("drop table if exists bronze.raw_customers;")
    con.execute(
        f"create table bronze.raw_customers as select * from read_parquet('{RAW_CUSTOMERS}');")

    con.execute("drop table if exists bronze.raw_vehicles;")
    con.execute(
        f"create table bronze.raw_vehicles as select * from read_parquet('{RAW_VEHICLES}');")

    con.execute("drop table if exists bronze.raw_eligibility_decisions;")
    con.execute(
        f"create table bronze.raw_eligibility_decisions as select * from read_parquet('{RAW_ELIG}');")

    con.execute("drop table if exists bronze.raw_leads;")
    con.execute(
        f"create table bronze.raw_leads as select * from read_parquet('{RAW_LEADS}');")

    con.execute("drop table if exists bronze.raw_purchases;")
    con.execute(
        f"create table bronze.raw_purchases as select * from read_parquet('{RAW_PURCHASES}');")

    # Materialized silver/gold tables using the versioned SQL definitions in pipelines/sql.
    with open("pipelines/sql/models.sql", "r", encoding="utf-8") as f:
        con.execute(f.read())

    with open("pipelines/sql/kpis.sql", "r", encoding="utf-8") as f:
        con.execute(f.read())

    con.close()
    print(f"Built DuckDB warehouse at {DB_PATH}")


if __name__ == "__main__":
    main()
