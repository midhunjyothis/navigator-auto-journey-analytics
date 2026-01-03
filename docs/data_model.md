# Data Model (v0)

## Guiding principles
- Every table declares its grain (what 1 row represents).
- Every fact table has a stable primary key.
- All joins flow through conformed dimensions (customer, vehicle, campaign, experiment).
- Events are append-only; all downstream tables are reproducible.

## Core entities (dimensions)

### dim_customer
- Grain: One row per unique known customer identity (latest state).
- Primary key: customer_id
- Notes: Anonymous users are not stored here and appear as anonymous_id in fact_events, linked via an identity bridge at login/pre-qual/lead. Modeled as Type 1 (latest attributes). Includes observed attributes from purchase data and derived/simulated fields (credit_score_band, income_band, segment) documented in the data dictionary.

### dim_vehicle
- Grain: One row per unique vehicle listing in the shopping universe.
- Primary key: vehicle_id
- Notes: vehicle_id is a stable surrogate key; VIN is masked or partially stored if present. Vehicle attributes are largely static; pricing and incentives are handled in separate pricing snapshot facts.

### dim_campaign
- Grain: One row per campaign configuration (channel, objective, creative).
- Primary key: campaign_id
- Notes: Used for attribution and trigger analysis. Campaign exposure is captured via fact_events. Includes start/end dates and targeting rules.

### dim_experiment
- Grain: One row per experiment definition.
- Primary key: experiment_id
- Notes: Stores hypothesis, primary metric, guardrails, randomization unit, and exposure surface. Variant assignment is captured in fact_events.

## Core facts

### fact_events
- Grain: One row per tracked user event (append-only).
- Primary key: event_id
- Foreign keys: customer_id (nullable), vehicle_id (nullable), campaign_id (nullable), experiment_id (nullable)
- Partitioning: event_date
- Notes: Stores anonymous_id and derived session_id. Canonical source for funnel entry, engagement, personalization exposure, and latency metrics.

### fact_eligibility_decision
- Grain: One row per eligibility decision returned.
- Primary key: eligibility_id
- Foreign keys: customer_id, vehicle_id (nullable), session_id (nullable)
- Notes: Includes prequal_flag, max_amount, apr_est, term_options, counteroffer_flag, and reason_codes. Multiple decisions per customer allowed; “current eligibility” defined downstream.

### fact_lead
- Grain: One row per submitted lead.
- Primary key: lead_id
- Foreign keys: customer_id (nullable), vehicle_id, campaign_id (nullable), experiment_id (nullable)
- Notes: Represents high-intent actions (contact dealer, schedule test drive, request quote). Dedup logic applied in marts for repeat submissions.

### fact_purchase
- Grain: One row per completed purchase transaction.
- Primary key: purchase_id
- Foreign keys: customer_id, vehicle_id, lead_id (nullable), campaign_id (nullable)
- Notes: Outcome table for north-star metrics. Attribution logic handled downstream; includes purchase_price and purchase_ts.

## Analytics marts

### mart_funnel_journey
- Grain: One row per customer–vehicle journey.
- Primary key: journey_id
- Built from: fact_events, fact_eligibility_decision, fact_lead, fact_purchase
- Notes: Canonical funnel table with stage flags, timestamps, and time-to-conversion metrics. All funnel KPIs sourced from this mart.

### mart_personalization_effect
- Grain: One row per experiment exposure unit (customer or session).
- Primary key: personalization_effect_id
- Built from: fact_events, dim_experiment, mart_funnel_journey
- Notes: Measures incremental lift of personalization on engagement, leads, and purchases with proper experiment windows and guardrails.