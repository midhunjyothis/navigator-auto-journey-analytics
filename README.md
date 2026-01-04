# Navigator Auto Journey Analytics

This project represents how I would design, build, and validate an end-to-end analytics platform for a digital auto-buying journey similar to Capital One’s Navigator platform.

I built this to demonstrate how I think about:
- customer journeys across anonymous → known states
- funnel measurement and latency
- experimentation and personalization lift
- governed metrics and data quality in a production-style setup

Everything here runs locally, but the structure mirrors what I would expect in a real cloud data platform.

---

## Problem I Solved

Digital auto buying is not a single event — it is a journey:
- customers browse anonymously
- eligibility is evaluated asynchronously
- intent shows up as leads
- purchases may happen much later

On top of that, personalization and experiments are constantly running.

I needed a data model that:
- preserves event-level truth
- rolls up cleanly to journey-level funnels
- supports experiment readouts without re-engineering
- makes data quality visible instead of assumed

This project is my answer to that.

---

## What I Built

### 1. Synthetic but Realistic Raw Data
I generated raw datasets that resemble production telemetry:
- customer attributes
- vehicle inventory
- behavioral events
- eligibility decisions
- leads
- purchases

The data intentionally includes:
- anonymous and logged-in users
- delayed conversions
- partial journeys
- experiment variants

This allowed me to validate modeling decisions, not just schemas.

---

### 2. Layered Warehouse Design (DuckDB)

I implemented a simple but disciplined layering model:

**Bronze (raw)**
- Immutable parquet files
- No business logic
- Mirrors source system grain

**Silver (conformed)**
- Cleaned dimensions and facts
- Standardized timestamps and keys
- No aggregation beyond entity grain

**Gold (analytics marts)**
- Journey-level funnel mart
- KPI and experiment readout views
- Designed for direct consumption

DuckDB was used intentionally to keep everything reproducible and local while still using real SQL.

---

### 3. Canonical Funnel Journey Mart

The core artifact is `gold.mart_funnel_journey`.

Each row represents:
> one customer/session/vehicle journey starting at first browse

From that single table I can answer:
- conversion rates
- time to eligibility
- time to purchase
- drop-off points
- experiment lift

This is the table I would expect downstream BI and experimentation teams to trust.

---

### 4. Experiment & KPI Readouts

I carried experiment and variant context into the gold layer so that:
- experiment analysis does not require event reprocessing
- KPIs are consistent across dashboards and analyses

I validated this by running direct SQL sanity checks showing lift between control and treatment variants.

---

### 5. Data Quality as Code

I added lightweight but meaningful data quality checks:
- primary key uniqueness
- referential integrity
- funnel monotonicity (no impossible sequences)

Failures produce an explicit report instead of silent corruption.

---

### 6. End-to-End Execution

The entire flow can be executed locally:
- raw data generation
- warehouse build
- data quality checks
- experiment readout

This mirrors how I think about ownership: analytics does not stop at a query.

---

## What This Demonstrates

From an analytics perspective, this project shows how I:
- think in terms of journeys, not tables
- design for experimentation from day one
- balance flexibility with governance
- validate assumptions with real outputs
- build things that other analysts can trust

From a technical perspective, it shows:
- SQL-first modeling
- Python used where it adds leverage
- deterministic, reproducible pipelines
- clear separation of concerns

---

## Why This Matters for Navigator-Style Platforms

Auto buying is high-consideration, asynchronous, and multi-touch.

If you cannot:
- reconcile anonymous and known behavior
- explain why conversion moved
- trust your experiment metrics

then personalization becomes guesswork.

This project is intentionally scoped, but the patterns scale.

---

## Status

**v1.0 – End-to-end complete**

The pipeline runs, metrics validate, and experiment lift is observable.

This is the version I would be comfortable walking through in an interview.

