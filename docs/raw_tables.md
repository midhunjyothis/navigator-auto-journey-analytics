# Raw Data Tables (Bronze Layer)

These tables represent immutable, append-only raw data as ingested.
No business logic is applied at this layer.

---

## raw_events
Grain:
- One row per user event

Core Fields:
- event_id (string, unique)
- event_ts (timestamp)
- event_date (date)
- event_type (string)
- customer_id (string, nullable)
- anonymous_id (string)
- session_id (string)
- vehicle_id (string, nullable)
- campaign_id (string, nullable)
- experiment_id (string, nullable)
- variant (string, nullable)
- platform (web/app)
- metadata (json)

Notes:
- Primary source for behavioral analytics.
- Immutable and append-only.

---

## raw_customers
Grain:
- One row per known customer

Core Fields:
- customer_id (string)
- state (string)
- zip3 (string)
- income_band (string)
- credit_score_band (string)
- customer_since (date)

Notes:
- Attributes represent latest known values.
- Derived fields documented separately.

---

## raw_vehicles
Grain:
- One row per vehicle listing

Core Fields:
- vehicle_id (string)
- make (string)
- model (string)
- year (int)
- body_type (string)
- msrp (numeric)

Notes:
- Pricing changes captured in pricing snapshots, not here.

---

## raw_eligibility_decisions
Grain:
- One row per eligibility decision

Core Fields:
- eligibility_id (string)
- customer_id (string)
- decision_ts (timestamp)
- approved_flag (boolean)
- max_amount (numeric)
- apr_est (numeric)
- reason_codes (array/string)

Notes:
- Multiple decisions per customer allowed.

---

## raw_leads
Grain:
- One row per submitted lead

Core Fields:
- lead_id (string)
- customer_id (string, nullable)
- vehicle_id (string)
- lead_ts (timestamp)
- lead_type (string)
- campaign_id (string, nullable)

Notes:
- Represents high-intent user actions.

---

## raw_purchases
Grain:
- One row per completed purchase

Core Fields:
- purchase_id (string)
- customer_id (string)
- vehicle_id (string)
- purchase_ts (timestamp)
- purchase_price (numeric)

Notes:
- Final outcome table.
