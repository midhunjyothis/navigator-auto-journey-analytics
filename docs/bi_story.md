# BI Story: End-to-End Digital Auto Buying Journey

This project focuses on answering a simple but high-impact question:

**Where do customers drop off in a digital car-buying journey, and how much does personalization actually move the needle?**

I built this as an end-to-end analytics system, from raw behavioral data to executive-ready insights, mirroring how a real digital auto platform like Capital One Navigator would operate.

---

## 1. Business Context

Buying a car digitally is not a single action. It is a journey:

1. Browse vehicles  
2. Check eligibility or financing  
3. Submit a lead  
4. Complete a purchase  

Each step introduces friction:
- uncertainty around eligibility
- pricing sensitivity
- decision fatigue
- personalization effectiveness

The goal of this analysis is to quantify friction, measure conversion, and evaluate whether personalization meaningfully improves outcomes.

---

## 2. Data Foundation

I generated a fully synthetic but realistic dataset to model this journey end-to-end.

### Why synthetic data?
- Avoids privacy and compliance concerns
- Allows full control over distributions and edge cases
- Enables repeatable experimentation
- Mirrors how internal test data is often created for analytics and ML development

### Core datasets:
- Customers (demographics, credit bands, tenure)
- Vehicles (make, model, MSRP)
- Events (browsing, clicks, engagement)
- Eligibility decisions (approval, APR, max amount)
- Leads
- Purchases

All data flows into a DuckDB warehouse and is modeled into bronze, silver, and gold layers, ensuring traceability and governance.

---

## 3. Funnel Dashboard: Where Customers Drop Off

### Primary Funnel
- Browse to Eligibility to Lead to Purchase

Key metrics surfaced:
- Conversion rate by stage
- Time between stages
- Funnel leakage points

**Key insight:**
The largest drop-off occurs between browsing and eligibility, not at purchase.  
This suggests financing uncertainty is a bigger blocker than vehicle choice.

If I owned this product, I would focus on:
- earlier eligibility previews
- soft-check signals during browse
- messaging that reduces financing anxiety upfront

---

## 4. Journey Latency and Experience

Beyond conversion, I analyzed time to progress:

- Minutes from browse to eligibility
- Minutes from browse to purchase

This highlights:
- where customers stall
- where decisions accelerate

Long latency combined with eventual drop-off indicates confusion, not lack of intent.

---

## 5. Personalization and Experimentation

I modeled a simple A/B test:
- Control: generic experience
- Treatment: personalized vehicle and pricing signals

### KPI used
- Purchase rate per journey

### Result (directional):
- Treatment shows a higher purchase rate than control
- Absolute lift is small, but statistically meaningful at scale

**Why this matters:**
In financial products, even a 0.01 to 0.05 percent lift compounds into real revenue when applied to millions of users.

This validates that:
- personalization should be measured carefully
- success is incremental, not dramatic
- experimentation must be built into the analytics foundation

---

## 6. Data Quality and Trust

To ensure decisions are reliable, I implemented:
- primary key uniqueness checks
- null checks on funnel-critical fields
- logical consistency checks, such as purchase without browse

Outputs are written to auditable reports, reinforcing trust in downstream dashboards.

---

## 7. Business Decisions Enabled

This analytics system directly supports decisions like:
- Where to invest UX improvements
- Whether personalization is worth scaling
- How eligibility messaging affects conversion
- Which funnel stages deserve experimentation

More importantly, it demonstrates how analytics moves from data to insight to decision, not just dashboards.

---

## 8. How I’d Explain This in 30 Seconds

> “I built an end-to-end analytics platform that models a digital car-buying journey from raw behavior to purchase.  
> It identifies where customers drop off, how long decisions take, and whether personalization actually improves conversion.  
> The result is a governed, experiment-ready system that turns customer behavior into product decisions.”
