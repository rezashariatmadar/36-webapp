# Track Specification: Coworking Space Reservations

## Overview
Implement a reservation system for coworking spaces (desks, offices, meeting rooms) with conflict detection and pricing logic.

## Requirements
- Manage multiple types of spaces (Zones).
- Support Hourly, Daily, and Monthly booking models.
- Prevent double-booking (Conflict Detection).
- Users can view availability and book spaces.
- Admin/Staff can manage spaces and prices.

## Technical Details
- App: `cowork`
- Models: `Space`, `PricingPlan`, `Booking`
- Logic: `Booking.clean()` for validation, `check_availability` utility (implemented in views/forms).
