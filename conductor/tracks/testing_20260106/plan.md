# Track Plan: Stability & Testing (v1.1)

## Phase 1: Environment & Tooling [checkpoint: b81f264]
- [x] Task: Install and Configure `factory_boy` e99b44e
    -   Install `factory_boy` using `uv`.
    -   Update `requirements.txt`.
- [x] Task: Setup Coverage Tooling e99b44e
    -   Install `coverage` or `pytest-cov`.
    -   Add configuration for coverage reporting.
- [x] Task: Conductor - User Manual Verification 'Environment & Tooling' (Protocol in workflow.md) b81f264

## Phase 2: URL Namespacing & Fixes [checkpoint: 8982cea]
- [x] Task: Audit & Fix URL Namespacing 8982cea
    -   Fix `NoReverseMatch` for 'logout'.
    -   Audit all templates for non-namespaced URLs.
    -   Audit all `redirect()` and `reverse()` calls in views.
- [x] Task: Regression Tests for URL Safety 8982cea
    -   Write tests to ensure core pages load.
    -   Verify no `NoReverseMatch` during test runs.
- [x] Task: Conductor - User Manual Verification 'URL Namespacing & Fixes' (Protocol in workflow.md) 8982cea

## Phase 3: Accounts Module Testing (RBAC & Auth)
- [ ] Task: Create Factories for Accounts
    -   `UserFactory` with support for different groups (Admin, Barista, Customer).
- [ ] Task: Implement Tests for National ID & Phone Validators
    -   Comprehensive unit tests for logic in `accounts/utils.py`.
- [ ] Task: Implement Tests for User Registration & Groups
    -   Test form submission and default group assignment.
- [ ] Task: Implement Tests for RBAC Decorators
    -   Verify that `@admin_required` and `@barista_required` restrict access correctly.
- [ ] Task: Conductor - User Manual Verification 'Accounts Module Testing' (Protocol in workflow.md)

## Phase 4: Cafe Module Testing (Menu & Orders)
- [ ] Task: Create Factories for Cafe
    -   `CategoryFactory`, `MenuItemFactory`, `OrderFactory`.
- [ ] Task: Implement Tests for Menu Logic
    -   Test category ordering and item availability filtering.
- [ ] Task: Implement Tests for Cart Session Logic
    -   Mock sessions to test add/remove/total logic.
- [ ] Task: Implement Tests for Order Management
    -   Test status transitions and manual order entry validation.
- [ ] Task: Conductor - User Manual Verification 'Cafe Module Testing' (Protocol in workflow.md)

## Phase 5: Coworking Module Testing (Spaces & Bookings)
- [ ] Task: Create Factories for Coworking
    -   `SpaceFactory`, `PricingPlanFactory`, `BookingFactory`.
- [ ] Task: Implement Tests for Availability Logic
    -   Test `check_availability` helper with overlapping scenarios.
- [ ] Task: Implement Tests for Pricing Logic
    -   Validate calculations for Daily, Monthly, and long-term plans.
- [ ] Task: Implement Tests for Operating Hours
    -   Ensure 8 AM - 8 PM constraints are enforced in `Booking.clean()`.
- [ ] Task: Conductor - User Manual Verification 'Coworking Module Testing' (Protocol in workflow.md)

## Phase 6: API & Coverage Finalization
- [ ] Task: Implement Tests for REST Endpoints
    -   Use `rest_framework.test` to verify User and Menu API responses.
- [ ] Task: Final Coverage Report & Cleanup
    -   Run full suite and ensure >80% coverage on all apps.
- [ ] Task: Conductor - User Manual Verification 'API & Coverage Finalization' (Protocol in workflow.md)
