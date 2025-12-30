# Data Model (v0)

## Guiding principles
- Every table declares its grain (what 1 row represents).
- Every fact table has a stable primary key.
- All joins flow through conformed dimensions (customer, vehicle, campaign, experiment).
- Events are append-only; all downstream tables are reproducible.

## Core entities (dimensions)

### dim_customer
- Grain: TODO
- Primary key: TODO
- Notes: TODO

### dim_vehicle
- Grain: TODO
- Primary key: TODO
- Notes: TODO

### dim_campaign
- Grain: TODO
- Primary key: TODO
- Notes: TODO

### dim_experiment
- Grain: TODO
- Primary key: TODO
- Notes: TODO

## Core facts

### fact_events
- Grain: TODO
- Primary key: TODO
- Foreign keys: TODO
- Partitioning: TODO
- Notes: TODO

### fact_eligibility_decision
- Grain: TODO
- Primary key: TODO
- Foreign keys: TODO
- Notes: TODO

### fact_lead
- Grain: TODO
- Primary key: TODO
- Foreign keys: TODO
- Notes: TODO

### fact_purchase
- Grain: TODO
- Primary key: TODO
- Foreign keys: TODO
- Notes: TODO

## Analytics marts

### mart_funnel_journey
- Grain: TODO
- Primary key: TODO
- Built from: TODO
- Notes: TODO

### mart_personalization_effect
- Grain: TODO
- Primary key: TODO
- Built from: TODO
- Notes: TODO
