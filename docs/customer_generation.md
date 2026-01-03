# Customer Generation Assumptions (v0)

## Purpose
Define realistic, explicit assumptions for generating synthetic customers
used in the Navigator Auto Journey analytics project.

These assumptions intentionally mirror patterns observed in real digital
auto shopping behavior without representing real individuals.

---

## Customer Volume
- Total customers generated: configurable (default: 50,000).
- A subset of customers will convert; most will not.

---

## Identity Model
- Each customer has a stable customer_id.
- Anonymous browsing occurs prior to identification and is handled outside
  this table via anonymous_id in raw_events.
- Identity stitching occurs at pre-qualification or lead submission.

---

## Geography
- Customers are distributed across U.S. states.
- State distribution is non-uniform to reflect population concentration.
- zip3 is derived from state-level distributions (approximate realism).

---

## Credit & Income Bands
- credit_score_band: {Subprime, Near Prime, Prime, Super Prime}
- income_band: {Low, Medium, High, Very High}

Assumptions:
- Credit and income are correlated but not perfectly.
- Prime and Near Prime make up the majority of customers.
- Subprime customers experience lower eligibility approval rates downstream.

---

## Segmentation
Derived segments used for analytics:
- value_seeker
- payment_focused
- premium_buyer
- undecided

Segments influence:
- vehicle price preference
- likelihood to start pre-qualification
- responsiveness to personalization

---

## Stability
- Customer attributes represent latest known state (Type 1).
- No intra-customer historical changes modeled in v0.
