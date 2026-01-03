# Data Quality & Governance (v0)

## Core Data Quality Checks

### Key Integrity
- All primary keys are non-null and unique.
- Foreign keys must resolve to valid dimension records where applicable.

### Event Completeness
- Daily volume checks on fact_events by event_type.
- Alert on sudden drops or spikes beyond expected thresholds.

### Funnel Consistency
- purchase_complete events must have a corresponding record in fact_purchase.
- submit_prequal events must have a corresponding eligibility decision.

### Duplicate Detection
- Detect duplicate leads for the same customer and vehicle within a short time window.
- Flag duplicate purchase events.

### Anomaly Detection
- Monitor approval rates, lead rates, and conversion rates for unexpected shifts.
- Segment-level anomaly checks (e.g., by credit band, channel).

---

## Governance & Definitions

### Metric Ownership
- Each KPI has a named owner responsible for definition changes.

### Change Management
- Metric changes require versioning and backfill strategy.

### Lineage
- All KPIs trace back to source facts and events.

### Access & Privacy
- Customer identifiers are masked or hashed.
- Sensitive attributes (credit bands) are stored as buckets, not raw values.
