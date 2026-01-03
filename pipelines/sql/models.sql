-- I conformed raw customer data into a single customer dimension
-- representing the latest known state per customer.

drop table if exists silver.dim_customer;
create table silver.dim_customer as
select
  customer_id,
  state,
  zip3,
  income_band,
  credit_score_band,
  segment,
  customer_since
from bronze.raw_customers;


-- I conformed raw vehicle listings into a vehicle dimension
-- and kept pricing snapshots out of this table intentionally.

drop table if exists silver.dim_vehicle;
create table silver.dim_vehicle as
select
  vehicle_id,
  make,
  model,
  year,
  body_type,
  msrp
from bronze.raw_vehicles;


-- I standardized raw events into a single fact table
-- used as the source of truth for funnel and engagement analytics.

drop table if exists silver.fact_events;
create table silver.fact_events as
select
  event_id,
  cast(event_ts as timestamp) as event_ts,
  cast(event_date as date) as event_date,
  event_type,
  customer_id,
  anonymous_id,
  session_id,
  vehicle_id,
  campaign_id,
  experiment_id,
  variant,
  platform,
  metadata
from bronze.raw_events;


-- I captured eligibility outcomes separately to avoid mixing
-- decision logic with behavioral events.

drop table if exists silver.fact_eligibility_decision;
create table silver.fact_eligibility_decision as
select
  eligibility_id,
  customer_id,
  cast(decision_ts as timestamp) as decision_ts,
  approved_flag,
  max_amount,
  apr_est,
  reason_codes
from bronze.raw_eligibility_decisions;


-- I stored submitted leads as their own fact table
-- since leads represent explicit high-intent actions.

drop table if exists silver.fact_lead;
create table silver.fact_lead as
select
  lead_id,
  customer_id,
  vehicle_id,
  cast(lead_ts as timestamp) as lead_ts,
  lead_type,
  campaign_id
from bronze.raw_leads;


-- I treated purchases as the final outcome table
-- used for all north-star and attribution metrics.

drop table if exists silver.fact_purchase;
create table silver.fact_purchase as
select
  purchase_id,
  customer_id,
  vehicle_id,
  cast(purchase_ts as timestamp) as purchase_ts,
  purchase_price
from bronze.raw_purchases;


-- I built a canonical funnel mart at the journey level
-- to support conversion, latency, and experiment analysis.

drop table if exists gold.mart_funnel_journey;
create table gold.mart_funnel_journey as
with browse as (
  select
    coalesce(customer_id, anonymous_id) as actor_id,
    customer_id,
    anonymous_id,
    session_id,
    vehicle_id,
    min(event_ts) as first_browse_ts
  from silver.fact_events
  where event_type = 'vehicle_view'
    and vehicle_id is not null
  group by 1,2,3,4,5
),
elig as (
  select
    customer_id,
    min(decision_ts) as eligibility_ts,
    max(case when approved_flag then 1 else 0 end) as approved_any
  from silver.fact_eligibility_decision
  group by 1
),
lead as (
  select
    customer_id,
    vehicle_id,
    min(lead_ts) as lead_ts
  from silver.fact_lead
  group by 1,2
),
purchase as (
  select
    customer_id,
    vehicle_id,
    min(purchase_ts) as purchase_ts,
    any_value(purchase_price) as purchase_price
  from silver.fact_purchase
  group by 1,2
)
select
  md5(
    coalesce(cast(b.customer_id as varchar),'') || '|' ||
    coalesce(cast(b.anonymous_id as varchar),'') || '|' ||
    coalesce(cast(b.session_id as varchar),'') || '|' ||
    coalesce(cast(b.vehicle_id as varchar),'') || '|' ||
    cast(b.first_browse_ts as varchar)
  ) as journey_id,
  b.customer_id,
  b.anonymous_id,
  b.session_id,
  b.vehicle_id,
  b.first_browse_ts,
  e.eligibility_ts,
  e.approved_any,
  l.lead_ts,
  p.purchase_ts,
  p.purchase_price,
  1 as reached_browse,
  case when e.eligibility_ts is not null then 1 else 0 end as reached_eligibility,
  case when l.lead_ts is not null then 1 else 0 end as reached_lead,
  case when p.purchase_ts is not null then 1 else 0 end as reached_purchase,
  case when e.eligibility_ts is not null then datediff('minute', b.first_browse_ts, e.eligibility_ts) end as mins_to_eligibility,
  case when p.purchase_ts is not null then datediff('minute', b.first_browse_ts, p.purchase_ts) end as mins_to_purchase
from browse b
left join elig e on e.customer_id = b.customer_id
left join lead l on l.customer_id = b.customer_id and l.vehicle_id = b.vehicle_id
left join purchase p on p.customer_id = b.customer_id and p.vehicle_id = b.vehicle_id;
