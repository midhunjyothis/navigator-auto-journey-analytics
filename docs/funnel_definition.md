# Funnel Definition (v0)

## Funnel Stages

### Browse
Definition:
- User triggers at least one `vehicle_view` event.

Notes:
- Entry point for funnel analytics.
- Measured at session and customer level.

### Eligibility
Definition:
- User triggers `submit_prequal`
- AND receives a record in `fact_eligibility_decision`.

Notes:
- Eligibility success defined separately (approved vs declined).
- Time-to-eligibility measured from first `vehicle_view`.

### Lead
Definition:
- User triggers `lead_submit`.

Notes:
- Lead types analyzed separately (contact, test drive, quote).
- Deduplication applied for repeat leads within journey.

### Purchase
Definition:
- User triggers `purchase_complete`
- AND has a matching record in `fact_purchase`.

Notes:
- Final funnel outcome.
- Attribution logic applied downstream.
