"""
I ran a small set of audit-friendly data quality checks against the DuckDB
warehouse to validate key integrity, funnel consistency, and basic null safety.

The goal was not exhaustive validation, but to establish baseline trust
in the analytics tables before using them for decisions.
"""

from __future__ import annotations

import json
import os
import duckdb

DB_PATH = os.environ.get("NAV_DB_PATH", "data/processed/navigator.duckdb")


def _single_value(con: duckdb.DuckDBPyConnection, sql: str):
    return con.execute(sql).fetchone()[0]


def main() -> None:
    con = duckdb.connect(DB_PATH)

    results = []

    # I validated primary key uniqueness on core tables.
    results.append({
        "check": "dim_customer.customer_id is unique",
        "status": "pass"
        if _single_value(con, "select count(*) = count(distinct customer_id) from silver.dim_customer")
        else "fail"
    })

    results.append({
        "check": "dim_vehicle.vehicle_id is unique",
        "status": "pass"
        if _single_value(con, "select count(*) = count(distinct vehicle_id) from silver.dim_vehicle")
        else "fail"
    })

    results.append({
        "check": "fact_events.event_id is unique",
        "status": "pass"
        if _single_value(con, "select count(*) = count(distinct event_id) from silver.fact_events")
        else "fail"
    })

    # I verified funnel consistency between events and outcome tables.
    results.append({
        "check": "purchase_complete events have matching purchases",
        "status": "pass"
        if _single_value(con, """
            select count(*) = 0
            from (
              select e.customer_id, e.vehicle_id
              from silver.fact_events e
              left join silver.fact_purchase p
                on p.customer_id = e.customer_id
               and p.vehicle_id = e.vehicle_id
              where e.event_type = 'purchase_complete'
                and e.customer_id is not null
                and p.purchase_id is null
              group by 1,2
            ) t
        """)
        else "fail"
    })

    # I checked for unexpected nulls on required event fields.
    results.append({
        "check": "fact_events.event_type has no nulls",
        "status": "pass"
        if _single_value(con, "select count(*) = 0 from silver.fact_events where event_type is null")
        else "fail"
    })

    con.close()

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/dq_report.json", "w", encoding="utf-8") as f:
        json.dump({"checks": results}, f, indent=2)

    print("Wrote data quality report to outputs/dq_report.json")


if __name__ == "__main__":
    main()
