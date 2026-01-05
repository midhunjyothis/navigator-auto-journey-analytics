# Tableau Public Dashboard: Digital Auto Buying Journey

This dashboard is a visual walkthrough of the analytics platform built in this project.

The goal is to make the full customer journey understandable without reading code, while still grounding every insight in real, modeled data.

## What the dashboard shows

### Funnel conversion by variant
This view compares purchase conversion between control and treatment experiences.  
It answers whether personalization has a measurable impact on outcomes.

### Daily journey volume
This shows how many customer journeys enter the funnel each day, split by variant.  
It validates that traffic allocation between control and treatment is balanced.

### Conversion trends over time
This view tracks purchase rate by day and variant.  
It helps distinguish real lift from noise and confirms whether treatment performance is consistent.

### Experience latency
This compares the average time from browse to eligibility and browse to purchase.  
It highlights whether personalization improves decision speed, not just conversion.

## Why the data is aggregated

The dashboard uses aggregated, journey-level metrics rather than raw event data.

This approach:
- protects privacy
- improves performance
- mirrors how external-facing analytics are typically shared
- keeps the focus on decisions, not implementation details

## How this would be used

This dashboard is designed for product managers and business leaders to:
- identify funnel bottlenecks
- evaluate experimentation results
- prioritize UX and messaging investments
- understand customer friction at scale
