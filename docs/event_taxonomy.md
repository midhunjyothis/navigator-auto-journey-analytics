# Event Taxonomy (v0)

## Principles
- Events represent observable user actions.
- Events are immutable and append-only.
- Funnel stages are derived from events, not hard-coded.

## Core Events

### page_view
User views any page in the Navigator experience.

### search
User performs a vehicle search or applies filters.

### vehicle_view
User views a vehicle detail page (VDP).
→ Primary funnel entry event.

### save_vehicle
User saves or favorites a vehicle.

### price_watch
User opts into price-drop notifications for a vehicle.

### start_prequal
User begins the eligibility / pre-qualification flow.

### submit_prequal
User submits eligibility information.
→ Eligibility stage entry.

### view_offer
User views personalized pricing or financing options.

### lead_submit
User submits a lead (dealer contact, test drive, quote).
→ Lead stage entry.

### purchase_complete
User completes a vehicle purchase.
→ Funnel completion.
