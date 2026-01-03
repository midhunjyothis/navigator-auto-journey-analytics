-- I created a consolidated KPI view to support executive-level
-- funnel monitoring and trend analysis.

drop view if exists gold.vw_funnel_kpis;
create view gold.vw_funnel_kpis as
with base as (
  select *
  from gold.mart_funnel_journey
)
select
  count(*) as total_journeys,

  avg(reached_eligibility)::double as browse_to_eligibility_rate,
  avg(reached_lead)::double as browse_to_lead_rate,
  avg(reached_purchase)::double as browse_to_purchase_rate,

  avg(case when reached_eligibility = 1 then reached_lead end)::double
    as eligibility_to_lead_rate,

  avg(case when reached_lead = 1 then reached_purchase end)::double
    as lead_to_purchase_rate,

  quantile_cont(mins_to_eligibility, 0.50) as median_minutes_to_eligibility,
  quantile_cont(mins_to_purchase, 0.50) as median_minutes_to_purchase
from base;


-- I created an experiment readout view to evaluate the
-- incremental impact of personalization on downstream outcomes.

drop view if exists gold.vw_experiment_readout;
create view gold.vw_experiment_readout as
select
  experiment_id,
  variant,
  count(distinct customer_id) as customers,
  avg(reached_lead)::double as lead_rate,
  avg(reached_purchase)::double as purchase_rate
from gold.mart_funnel_journey
where experiment_id is not null
group by 1, 2;
