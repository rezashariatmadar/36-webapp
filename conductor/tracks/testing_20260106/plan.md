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

## Phase 3: Unit Tests (Models & Validation) [checkpoint: 12321ed]
- [x] Task: Create `factory_boy` Factories 07a2366
    -   UserFactory
    -   MenuItemFactory
    -   SpaceFactory
    -   BookingFactory
- [x] Task: Unit Tests for National ID & Phone Validation 07a2366
    -   Implement comprehensive tests for `validate_iranian_national_id`.
    -   Test `CustomUser` phone number validation.
- [x] Task: Unit Tests for Cafe Logic (Cart & Orders) 8982cea
    -   Test cart session logic (add/remove/total).
    -   Test order status transitions.
    -   Verify menu category ordering.
- [x] Task: Unit Tests for Coworking Logic (Spaces & Bookings) 12321ed
    -   Test space availability checks & conflict prevention.
    -   Validate pricing calculations for all plans.
    -   Enforce 08:00-20:00 operating hour constraints.
- [x] Task: Conductor - User Manual Verification 'Models & Validation' (Protocol in workflow.md) 12321ed

## Phase 4: RBAC & Permission Testing
- [x] Task: Unit Tests for RBAC Decorators 12321ed
    -   Test `admin_required` with different user roles.
    -   Test `barista_required` with different user roles.
    -   Verify redirect to login for unauthenticated users.
- [x] Task: Conductor - User Manual Verification 'RBAC & Permission Testing' (Protocol in workflow.md) 12321ed

## Phase 5: API Testing & Coverage Finalization [checkpoint: 099cf1a]
- [x] Task: Implement Tests for REST Endpoints 12321ed
    -   Use `rest_framework.test` to verify User and Menu API responses.
- [x] Task: Final Coverage Report & Cleanup 099cf1a
    -   Run full suite and ensure >80% coverage on all apps.
- [x] Task: Conductor - User Manual Verification 'API & Coverage Finalization' (Protocol in workflow.md) 099cf1a
