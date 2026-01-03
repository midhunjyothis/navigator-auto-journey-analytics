"""
I generated a compact A/B readout for the personalization experiment.

I focused on business outcomes (lead_rate, purchase_rate) and reported:
- per-variant rates
- the lift (treatment - control)
- a simple confidence interval for the lift (difference in proportions)

This was intentionally lightweight, reproducible, and easy to explain in a panel review.
"""

from __future__ import annotations

import os
import duckdb
import pandas as pd
import numpy as np

DB_PATH = os.environ.get("NAV_DB_PATH", "data/processed/navigator.duckdb")


def _diff_in_proportions_ci(control_rate: float, control_n: int,
                            treatment_rate: float, treatment_n: int,
                            z: float = 1.96):
    """
    I used a pooled-proportion normal approximation to compute a CI for the lift.
    This is appropriate for large n and keeps the readout explainable.
    """
    x1 = control_rate * control_n
    x2 = treatment_rate * treatment_n
    p_pool = (x1 + x2) / (control_n + treatment_n)

    se = np.sqrt(p_pool * (1 - p_pool) * (1 / control_n + 1 / treatment_n))
    lift = treatment_rate - control_rate
    return float(lift), float(lift - z * se), float(lift + z * se)


def main() -> None:
    con = duckdb.connect(DB_PATH)
    df = con.execute(
        "select * from gold.vw_experiment_readout order by variant"
    ).fetchdf()
    con.close()

    if set(df["variant"].tolist()) != {"control", "treatment"}:
        raise ValueError(
            "Expected exactly two variants: control and treatment")

    control = df[df["variant"] == "control"].iloc[0]
    treatment = df[df["variant"] == "treatment"].iloc[0]

    out_rows = []
    for metric in ["lead_rate", "purchase_rate"]:
        lift, ci_low, ci_high = _diff_in_proportions_ci(
            float(control[metric]), int(control["customers"]),
            float(treatment[metric]), int(treatment["customers"])
        )
        out_rows.append({
            "experiment_id": str(control["experiment_id"]),
            "metric": metric,
            "control_rate": float(control[metric]),
            "treatment_rate": float(treatment[metric]),
            "lift": lift,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "control_n": int(control["customers"]),
            "treatment_n": int(treatment["customers"]),
        })

    os.makedirs("outputs", exist_ok=True)
    pd.DataFrame(out_rows).to_csv(
        "outputs/experiment_readout.csv", index=False)
    print("Wrote experiment readout to outputs/experiment_readout.csv")


if __name__ == "__main__":
    main()
