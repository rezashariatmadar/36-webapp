# Track Plan: Coworking Space Reservations

## Phase 1: Backend Foundation
- [x] Task: Create Cowork App & Models
    -   `PricingPlan`, `Space`, `Booking`.
    -   Validation logic for end_time > start_time and overlapping bookings.
- [x] Task: Data Seeding
    -   Management command `seed_spaces` to populate 40+ units.

## Phase 2: User Interface (v1 - List Based)
- [x] Task: Space Discovery View
    -   List all spaces with filtering by Zone.
    -   Date-based availability filtering.
- [x] Task: Booking Flow
    -   Booking form with start/end time inputs.
    -   Confirmation and error handling.
- [x] Task: User Dashboard
    -   "My Bookings" list view.

## Phase 3: Interactive Map (v2 - Deferred)
- [ ] Task: Floor Plan Overlay
    -   CSS Grid/Canvas implementation.
    -   Real-time status indicators.
