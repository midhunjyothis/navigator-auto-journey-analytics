"""
I generated raw (bronze-layer) datasets for the Navigator Auto Journey analytics project.

This module produced deterministic, realistic synthetic data for:
- raw_customers
- raw_vehicles
- raw_events
- raw_eligibility_decisions
- raw_leads
- raw_purchases

The generation logic followed the assumptions in /docs and was intended to
support funnel KPIs, personalization experiments, and data quality validation.
"""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


RANDOM_SEED = 42
DEFAULT_CUSTOMER_COUNT = 50_000
DEFAULT_VEHICLE_COUNT = 25_000
DEFAULT_DAYS = 60
DEFAULT_EVENT_TARGET = 800_000


def set_seed(seed: int = RANDOM_SEED) -> None:
    """I set deterministic seeds so the same inputs produced the same datasets."""
    random.seed(seed)
    np.random.seed(seed)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _weighted_choice(rng: np.random.Generator, items: List[str], weights: List[float], size: int) -> np.ndarray:
    w = np.array(weights, dtype=float)
    w = w / w.sum()
    return rng.choice(items, size=size, replace=True, p=w)


def generate_raw_customers(n_customers: int, seed: int) -> pd.DataFrame:
    """I generated one row per known customer (latest-state), aligned to raw_customers."""
    set_seed(seed)
    rng = np.random.default_rng(seed)

    states = ["CA","TX","FL","NY","PA","IL","OH","GA","NC","MI","NJ","VA","WA","AZ","MA","TN","IN","MO","MD","WI"]
    state_w = [0.12,0.09,0.07,0.06,0.04,0.04,0.04,0.035,0.035,0.03,0.03,0.03,0.03,0.03,0.025,0.025,0.02,0.02,0.02,0.02]
    state = _weighted_choice(rng, states, state_w, n_customers)

    zip3 = rng.integers(100, 999, size=n_customers).astype(str)

    income_bands = ["Low", "Medium", "High", "Very High"]
    income_w = [0.25, 0.45, 0.22, 0.08]
    income_band = _weighted_choice(rng, income_bands, income_w, n_customers)

    credit_bands = ["Subprime", "Near Prime", "Prime", "Super Prime"]
    base = np.array([0.18, 0.30, 0.37, 0.15], dtype=float)

    credit_band = []
    for ib in income_band:
        if ib == "Low":
            w = base + np.array([0.10, 0.05, -0.10, -0.05])
        elif ib == "Medium":
            w = base + np.array([0.03, 0.03, -0.04, -0.02])
        elif ib == "High":
            w = base + np.array([-0.05, -0.02, 0.04, 0.03])
        else:
            w = base + np.array([-0.08, -0.04, 0.05, 0.07])
        w = np.clip(w, 0.01, None)
        w = w / w.sum()
        credit_band.append(rng.choice(credit_bands, p=w))
    credit_band = np.array(credit_band)

    segments = ["value_seeker", "payment_focused", "premium_buyer", "undecided"]
    seg_w = [0.34, 0.30, 0.16, 0.20]
    segment = _weighted_choice(rng, segments, seg_w, n_customers)

    now = _utc_now().date()
    days_back = rng.integers(30, 3650, size=n_customers)
    customer_since = pd.to_datetime([now - timedelta(days=int(d)) for d in days_back]).date

    return pd.DataFrame({
        "customer_id": [f"c_{i:07d}" for i in range(1, n_customers + 1)],
        "state": state,
        "zip3": zip3,
        "income_band": income_band,
        "credit_score_band": credit_band,
        "customer_since": customer_since,
        "segment": segment,
    })


def generate_raw_vehicles(n_vehicles: int, seed: int) -> pd.DataFrame:
    """I generated one row per vehicle listing, aligned to raw_vehicles."""
    set_seed(seed)
    rng = np.random.default_rng(seed + 11)

    makes = ["Toyota","Honda","Ford","Chevrolet","Nissan","Hyundai","Kia","BMW","Mercedes-Benz","Audi","Tesla","Jeep","Subaru","Volkswagen","Mazda","Lexus"]
    make_w = [0.12,0.10,0.10,0.09,0.07,0.07,0.06,0.05,0.04,0.04,0.03,0.06,0.05,0.04,0.04,0.04]
    make = _weighted_choice(rng, makes, make_w, n_vehicles)

    models_by_make = {
        "Toyota":["Camry","Corolla","RAV4","Highlander","Tacoma"],
        "Honda":["Civic","Accord","CR-V","Pilot"],
        "Ford":["F-150","Escape","Explorer","Mustang"],
        "Chevrolet":["Silverado","Equinox","Malibu","Tahoe"],
        "Nissan":["Altima","Sentra","Rogue","Pathfinder"],
        "Hyundai":["Elantra","Sonata","Tucson","Santa Fe"],
        "Kia":["Forte","K5","Sportage","Sorento"],
        "BMW":["3 Series","X3","X5"],
        "Mercedes-Benz":["C-Class","GLC","E-Class"],
        "Audi":["A4","Q5","A6"],
        "Tesla":["Model 3","Model Y","Model S"],
        "Jeep":["Wrangler","Grand Cherokee","Compass"],
        "Subaru":["Outback","Forester","Crosstrek"],
        "Volkswagen":["Jetta","Tiguan","Atlas"],
        "Mazda":["Mazda3","CX-5","CX-9"],
        "Lexus":["ES","RX","NX"],
    }
    model = np.array([rng.choice(models_by_make[m]) for m in make])

    year = rng.integers(2015, 2026, size=n_vehicles)

    body = np.array([
        "SUV" if m in ["RAV4","Highlander","CR-V","Pilot","Escape","Explorer","Rogue","Pathfinder","Tucson","Santa Fe","Sportage","Sorento","X3","X5","GLC","Q5","Model Y","Grand Cherokee","Compass","Outback","Forester","Crosstrek","Tiguan","Atlas","CX-5","CX-9","RX","NX"] else
        "Truck" if m in ["F-150","Silverado","Tacoma"] else
        "Coupe" if m in ["Mustang"] else
        "Hatchback" if m in ["Mazda3"] else
        "Sedan"
        for m in model
    ])

    base = np.where(body == "Truck", 42000, np.where(body == "SUV", 38000, 28000)).astype(float)
    premium_make = np.isin(make, ["BMW","Mercedes-Benz","Audi","Lexus","Tesla"])
    base = base + np.where(premium_make, 18000, 0)
    base = base + np.where(make == "Tesla", 12000, 0)

    age = (2026 - year).astype(float)
    msrp = base - age * np.random.default_rng(seed + 12).normal(900, 200, size=n_vehicles) + rng.normal(0, 2500, size=n_vehicles)
    msrp = np.clip(msrp, 9000, 95000).round(0)

    return pd.DataFrame({
        "vehicle_id": [f"v_{i:07d}" for i in range(1, n_vehicles + 1)],
        "make": make,
        "model": model,
        "year": year,
        "body_type": body,
        "msrp": msrp,
    })


def _approval_probability(credit_band: str, price: float) -> float:
    base = {"Subprime": 0.35, "Near Prime": 0.58, "Prime": 0.76, "Super Prime": 0.88}[credit_band]
    adj = -0.0000035 * max(price - 25000, 0)
    return float(np.clip(base + adj, 0.05, 0.97))


def _intent_parameters(segment: str) -> Tuple[float, float]:
    if segment == "payment_focused":
        return 0.22, 0.30
    if segment == "value_seeker":
        return 0.18, 0.26
    if segment == "premium_buyer":
        return 0.28, 0.34
    return 0.12, 0.22


def generate_events_and_outcomes(
    customers: pd.DataFrame,
    vehicles: pd.DataFrame,
    days: int,
    event_target: int,
    seed: int,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    I simulated browsing → (optional) prequal → (optional) lead → (optional) purchase.
    I embedded a simple A/B flag (control vs treatment) to support experimentation.
    """
    set_seed(seed)
    rng = np.random.default_rng(seed + 21)

    now = _utc_now()
    start = now - timedelta(days=days)

    experiment_id = "exp_personalization_v0"
    variants = ["control", "treatment"]

    cust_ids = customers["customer_id"].values
    cust_variant = rng.choice(variants, size=len(cust_ids), p=[0.50, 0.50])
    variant_map = dict(zip(cust_ids, cust_variant))

    campaign_ids = ["cmp_email_trigger", "cmp_push_trigger", "cmp_paid_search"]
    camp_w = [0.35, 0.25, 0.40]

    anon_share = 0.40

    vehicle_ids = vehicles["vehicle_id"].values
    vehicle_prices: Dict[str, float] = vehicles.set_index("vehicle_id")["msrp"].to_dict()

    events = []
    elig = []
    leads = []
    purchases = []

    event_seq = 1
    elig_seq = 1
    lead_seq = 1
    purchase_seq = 1

    while len(events) < event_target:
        c = rng.choice(cust_ids)
        c_row = customers.loc[customers["customer_id"] == c].iloc[0]
        seg = str(c_row["segment"])
        credit = str(c_row["credit_score_band"])

        is_anon = bool(rng.random() < anon_share)
        anonymous_id = f"a_{rng.integers(1, 25_000_000):08d}"
        customer_id = None if is_anon else c

        sess_start = start + timedelta(seconds=int(rng.integers(0, days * 86400)))
        session_id = f"s_{rng.integers(1, 9_000_000):07d}"
        platform = rng.choice(["web", "app"], p=[0.62, 0.38])

        exp_variant = variant_map[c] if not is_anon else rng.choice(variants)
        personalization = bool(exp_variant == "treatment")

        campaign_id = rng.choice(campaign_ids, p=np.array(camp_w) / np.sum(camp_w)) if rng.random() < 0.25 else None

        for etype in ["page_view", "search"]:
            t = sess_start + timedelta(seconds=int(rng.integers(1, 45)))
            events.append({
                "event_id": f"e_{event_seq:09d}",
                "event_ts": t.isoformat(),
                "event_date": t.date().isoformat(),
                "event_type": etype,
                "customer_id": customer_id,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "vehicle_id": None,
                "campaign_id": campaign_id,
                "experiment_id": experiment_id,
                "variant": exp_variant,
                "platform": platform,
                "metadata": json.dumps({"personalization": personalization}),
            })
            event_seq += 1

        n_views = int(rng.integers(1, 7))
        viewed = rng.choice(vehicle_ids, size=n_views, replace=False)

        t = sess_start + timedelta(seconds=60)
        saved_any = False
        watched_any = False
        chosen_vehicle = None

        for v in viewed:
            chosen_vehicle = v if chosen_vehicle is None else chosen_vehicle

            events.append({
                "event_id": f"e_{event_seq:09d}",
                "event_ts": t.isoformat(),
                "event_date": t.date().isoformat(),
                "event_type": "vehicle_view",
                "customer_id": customer_id,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "vehicle_id": v,
                "campaign_id": campaign_id,
                "experiment_id": experiment_id,
                "variant": exp_variant,
                "platform": platform,
                "metadata": json.dumps({
                    "personalization": personalization,
                    "rec_rank": int(rng.integers(1, 21)) if personalization else None,
                    "latency_ms": int(np.clip(rng.normal(420, 120), 80, 2000)),
                }),
            })
            event_seq += 1
            t += timedelta(seconds=int(rng.integers(15, 55)))

            if rng.random() < (0.10 + (0.03 if personalization else 0.0)):
                saved_any = True
                events.append({
                    "event_id": f"e_{event_seq:09d}",
                    "event_ts": t.isoformat(),
                    "event_date": t.date().isoformat(),
                    "event_type": "save_vehicle",
                    "customer_id": customer_id,
                    "anonymous_id": anonymous_id,
                    "session_id": session_id,
                    "vehicle_id": v,
                    "campaign_id": campaign_id,
                    "experiment_id": experiment_id,
                    "variant": exp_variant,
                    "platform": platform,
                    "metadata": json.dumps({"personalization": personalization}),
                })
                event_seq += 1
                t += timedelta(seconds=int(rng.integers(10, 30)))

            if rng.random() < 0.06:
                watched_any = True
                events.append({
                    "event_id": f"e_{event_seq:09d}",
                    "event_ts": t.isoformat(),
                    "event_date": t.date().isoformat(),
                    "event_type": "price_watch",
                    "customer_id": customer_id,
                    "anonymous_id": anonymous_id,
                    "session_id": session_id,
                    "vehicle_id": v,
                    "campaign_id": campaign_id,
                    "experiment_id": experiment_id,
                    "variant": exp_variant,
                    "platform": platform,
                    "metadata": json.dumps({"personalization": personalization}),
                })
                event_seq += 1
                t += timedelta(seconds=int(rng.integers(10, 30)))

        chosen_vehicle = chosen_vehicle or rng.choice(vehicle_ids)
        price = float(vehicle_prices.get(chosen_vehicle, 30000.0))

        start_prequal_prob, lead_given_prequal = _intent_parameters(seg)
        start_prequal_prob += 0.03 if personalization else 0.0
        did_prequal = bool(rng.random() < start_prequal_prob)

        if did_prequal:
            resolved_customer_id = c

            events.append({
                "event_id": f"e_{event_seq:09d}",
                "event_ts": t.isoformat(),
                "event_date": t.date().isoformat(),
                "event_type": "start_prequal",
                "customer_id": resolved_customer_id,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "vehicle_id": chosen_vehicle,
                "campaign_id": campaign_id,
                "experiment_id": experiment_id,
                "variant": exp_variant,
                "platform": platform,
                "metadata": json.dumps({"personalization": personalization}),
            })
            event_seq += 1
            t += timedelta(seconds=int(rng.integers(20, 90)))

            events.append({
                "event_id": f"e_{event_seq:09d}",
                "event_ts": t.isoformat(),
                "event_date": t.date().isoformat(),
                "event_type": "submit_prequal",
                "customer_id": resolved_customer_id,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "vehicle_id": chosen_vehicle,
                "campaign_id": campaign_id,
                "experiment_id": experiment_id,
                "variant": exp_variant,
                "platform": platform,
                "metadata": json.dumps({"personalization": personalization}),
            })
            event_seq += 1
            t += timedelta(seconds=int(rng.integers(10, 40)))

            approved = bool(rng.random() < _approval_probability(credit, price))
            max_amount = float(np.clip(rng.normal(price * (0.85 if approved else 0.65), price * 0.12), 5000, 100000))
            apr = float(np.clip(rng.normal(7.0 if approved else 13.0, 2.0), 1.9, 29.9))

            reason_codes: List[str] = []
            if not approved:
                reason_codes = rng.choice(
                    ["DTI_HIGH", "CREDIT_FILE_THIN", "INCOME_INSUFFICIENT", "VEHICLE_PRICE_HIGH"],
                    size=int(rng.integers(1, 3)),
                    replace=False
                ).tolist()

            elig.append({
                "eligibility_id": f"el_{elig_seq:09d}",
                "customer_id": resolved_customer_id,
                "decision_ts": t.isoformat(),
                "approved_flag": approved,
                "max_amount": round(max_amount, 2),
                "apr_est": round(apr, 2),
                "reason_codes": json.dumps(reason_codes),
            })
            elig_seq += 1

            events.append({
                "event_id": f"e_{event_seq:09d}",
                "event_ts": (t + timedelta(seconds=10)).isoformat(),
                "event_date": t.date().isoformat(),
                "event_type": "view_offer",
                "customer_id": resolved_customer_id,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "vehicle_id": chosen_vehicle,
                "campaign_id": campaign_id,
                "experiment_id": experiment_id,
                "variant": exp_variant,
                "platform": platform,
                "metadata": json.dumps({"personalization": personalization, "approved": approved}),
            })
            event_seq += 1
            t += timedelta(seconds=int(rng.integers(10, 50)))

            did_lead = bool((approved and rng.random() < lead_given_prequal) or (not approved and rng.random() < 0.07))
            if did_lead:
                lead_type = rng.choice(["contact_dealer", "schedule_test_drive", "request_quote"], p=[0.50, 0.30, 0.20])

                events.append({
                    "event_id": f"e_{event_seq:09d}",
                    "event_ts": t.isoformat(),
                    "event_date": t.date().isoformat(),
                    "event_type": "lead_submit",
                    "customer_id": resolved_customer_id,
                    "anonymous_id": anonymous_id,
                    "session_id": session_id,
                    "vehicle_id": chosen_vehicle,
                    "campaign_id": campaign_id,
                    "experiment_id": experiment_id,
                    "variant": exp_variant,
                    "platform": platform,
                    "metadata": json.dumps({"lead_type": lead_type, "personalization": personalization}),
                })
                event_seq += 1

                leads.append({
                    "lead_id": f"l_{lead_seq:09d}",
                    "customer_id": resolved_customer_id,
                    "vehicle_id": chosen_vehicle,
                    "lead_ts": t.isoformat(),
                    "lead_type": str(lead_type),
                    "campaign_id": campaign_id,
                })
                lead_seq += 1

                base_buy = 0.045 + (0.012 if personalization else 0.0)
                base_buy += 0.020 if approved else -0.020
                base_buy += 0.010 if saved_any else 0.0
                base_buy += 0.008 if watched_any else 0.0
                base_buy = float(np.clip(base_buy, 0.002, 0.22))

                if rng.random() < base_buy:
                    purchase_ts = t + timedelta(days=int(rng.integers(0, 15)), hours=int(rng.integers(1, 20)))
                    purchase_price = float(np.clip(rng.normal(price * 0.96, price * 0.05), 5000, 120000))

                    purchases.append({
                        "purchase_id": f"p_{purchase_seq:09d}",
                        "customer_id": resolved_customer_id,
                        "vehicle_id": chosen_vehicle,
                        "purchase_ts": purchase_ts.isoformat(),
                        "purchase_price": round(purchase_price, 2),
                    })
                    purchase_seq += 1

                    events.append({
                        "event_id": f"e_{event_seq:09d}",
                        "event_ts": purchase_ts.isoformat(),
                        "event_date": purchase_ts.date().isoformat(),
                        "event_type": "purchase_complete",
                        "customer_id": resolved_customer_id,
                        "anonymous_id": anonymous_id,
                        "session_id": session_id,
                        "vehicle_id": chosen_vehicle,
                        "campaign_id": campaign_id,
                        "experiment_id": experiment_id,
                        "variant": exp_variant,
                        "platform": platform,
                        "metadata": json.dumps({"purchase_price": round(purchase_price, 2), "personalization": personalization}),
                    })
                    event_seq += 1

    return pd.DataFrame(events), pd.DataFrame(elig), pd.DataFrame(leads), pd.DataFrame(purchases)


def _write_parquet(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)


def main() -> None:
    seed = int(os.environ.get("NAV_SEED", RANDOM_SEED))
    n_customers = int(os.environ.get("NAV_CUSTOMERS", DEFAULT_CUSTOMER_COUNT))
    n_vehicles = int(os.environ.get("NAV_VEHICLES", DEFAULT_VEHICLE_COUNT))
    days = int(os.environ.get("NAV_DAYS", DEFAULT_DAYS))
    event_target = int(os.environ.get("NAV_EVENT_TARGET", DEFAULT_EVENT_TARGET))

    customers = generate_raw_customers(n_customers=n_customers, seed=seed)
    vehicles = generate_raw_vehicles(n_vehicles=n_vehicles, seed=seed)
    events, elig, leads, purchases = generate_events_and_outcomes(
        customers=customers,
        vehicles=vehicles,
        days=days,
        event_target=event_target,
        seed=seed,
    )

    _write_parquet(customers, "data/raw/raw_customers.parquet")
    _write_parquet(vehicles, "data/raw/raw_vehicles.parquet")
    _write_parquet(events, "data/raw/raw_events.parquet")
    _write_parquet(elig, "data/raw/raw_eligibility_decisions.parquet")
    _write_parquet(leads, "data/raw/raw_leads.parquet")
    _write_parquet(purchases, "data/raw/raw_purchases.parquet")

    print("Wrote raw parquet files to data/raw/")
    print(
        f"customers={len(customers):,} vehicles={len(vehicles):,} "
        f"events={len(events):,} elig={len(elig):,} leads={len(leads):,} purchases={len(purchases):,}"
    )


if __name__ == "__main__":
    main()
