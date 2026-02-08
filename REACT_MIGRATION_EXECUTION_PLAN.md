# React Migration Execution Plan

Date: 2026-02-08  
Owner: Engineering  
Scope: Migrate frontend UX from mixed Django templates + HTMX/Alpine/jQuery to a React app shell served by Django, while preserving backend business logic and permission controls.

## 1. Objectives

- Consolidate UI execution into React so feature work no longer duplicates logic across templates and islands.
- Keep Django as backend authority for auth/session, role-based permissions, domain logic, and admin.
- Migrate incrementally with low-risk cutover, keeping legacy routes available until parity is proven.
- Remove obsolete frontend stack components after parity to reduce maintenance cost.

## 2. Architecture Decisions (Locked)

- Frontend delivery model: single React app served by Django static/template pipeline.
- Auth model: Django session + CSRF (same-origin APIs).
- Cutover strategy: staged (`/app` first), then move route ownership.
- API strategy: explicit `/api/auth/*`, `/api/cafe/*`, `/api/cowork/*` contracts.
- Backward compatibility: legacy template routes remain during migration.

## 3. Current State Snapshot

### Completed

- `/app` shell is implemented and routed.
- New API namespaces are implemented:
  - `/api/auth/me/`
  - `/api/cafe/menu|cart|cart/items|checkout|orders|orders/{id}/reorder`
  - `/api/cowork/spaces|bookings/preview|bookings|my-bookings`
- React SPA scaffold is implemented in `theme/static_src/src/spa/`.
- Build chain emits `spa-app.js` and `spa-app.css`.
- CSP debug connect-src allows local SPA dev tooling.
- Regression tests added for new auth/cafe/cowork APIs and SPA shell mount.
- Session auth/account APIs expanded with login, logout, register, and profile contracts.
- React account route is implemented at `/app/account` with SPA-native auth/profile UI.
- Root cutover routing now serves SPA-first paths by default.
- Legacy route fallback path added under `/legacy/*` for safe rollback operations.
- Legacy account auth/profile paths under `/legacy/*` now redirect to `/app/account`.
- Legacy account template auth/profile implementation has been removed (routes are redirect-only for compatibility).
- Expanded regression coverage for migration APIs and cutover behavior; full suite currently green.
- Alpine.js template directives and CDN dependency removed from runtime templates.
- jQuery/Persian datepicker assets removed from global base template and scoped to legacy booking form only.
- Default-mode `/cafe/*` and `/cowork/*` now redirect into `/legacy/*` ownership.
- HTMX runtime script and body `hx-headers` wiring have been removed from template runtime.
- Server-side HTMX partial response branches have been removed from `cafe` and `cowork` views.
- `django-htmx` app/middleware wiring removed from runtime settings; legacy HTMX detection now uses request headers.
- `django-htmx` dependency has been removed from project manifests (`pyproject.toml`, `uv.lock`).
- React Bits runtime assets and mount containers have been removed from template runtime (`base.html` and legacy UI fragments now use static markup).
- jQuery/Persian datepicker runtime assets have been removed from legacy booking template flow (`theme/templates/cowork/book_space.html`).

### In Progress

- Expanded SPA navigation and role-aware surfaces.

### Not Started

- Hard removal of remaining transitional legacy admin routes after staff/admin parity sign-off.
- Cleanup of redirect-only legacy account aliases once external deep-link compatibility requirements are closed.

## 4. Migration Phases

## Phase 0: Foundation and Contracts (Done)

Deliverables:
- App shell route and template.
- Session bootstrap contract (`/api/auth/me/`).
- Cafe and cowork customer contracts.
- Baseline test coverage and build integration.

Exit criteria:
- API contracts stable and tested.
- App shell reachable and functional in prod build.

## Phase 1: Customer Flows on React (In Progress)

Deliverables:
- Cafe customer flow: menu, cart, checkout, order history, reorder.
- Cowork customer flow: spaces list, price preview, booking create, my bookings.
- Role-aware app shell and route navigation.

Exit criteria:
- Customer usage does not require HTMX interactions in migrated routes.
- API/UX parity for main happy paths.

## Phase 2: Staff and Admin Flows (In Progress)

Deliverables:
- Staff active orders API with status/payment mutation APIs.
- Staff menu stock management APIs.
- React staff dashboard route and controls.
- Customer lookup API for barista workflow.

Exit criteria:
- Barista daily operations can run from `/app` routes.
- Permission checks enforced server-side and covered by tests.

## Phase 3: Account Experience Consolidation (In Progress)

Deliverables:
- Optional SPA account/profile pages using APIs.
- Decision point: keep server auth pages or migrate auth forms to SPA.

Exit criteria:
- Account flows consistent with app shell UX.

## Phase 4: Route Cutover and Decommission (Planned)

Deliverables:
- Route ownership switch from template pages to SPA entry.
- Redirect policy for legacy endpoints.
- Removal of unused template partials and JS dependencies.

Exit criteria:
- `/` primarily serves SPA shell (except admin/media/static/system paths).
- No production dependency on HTMX/Alpine/jQuery for core flows.

## Phase 5: Hardening and Cleanup (Planned)

Deliverables:
- Security hardening on CSP once inline legacy scripts are removed.
- Dead-code cleanup across templates/static files.
- Final documentation refresh and maintenance playbook.

Exit criteria:
- Lean frontend stack, stable tests, reduced bundle/dependency surface.

## 5. API Contract Rules

- Use JSON objects only (no HTML partial responses for SPA endpoints).
- Preserve stable key names once released; add keys backward-compatibly.
- Validate permissions on server for every mutating endpoint.
- Return clear `detail` messages for error states.

## 6. Testing and Validation Plan

- Targeted pytest per phase (new APIs and permission checks).
- Full `uv run pytest` after each significant increment.
- Production build validation with `npm run build`.
- Browser-level smoke checks via Playwright snapshots/screenshots when UI behavior changes materially.

## 7. Rollback Strategy

- Keep legacy account routes operational under `/legacy/*` during transition.
- Use checkpoint refs before destructive route removals (commit + backup branch + tag).
- If regressions occur after route removals, roll back to checkpoint refs and re-apply fixes in a new forward patch.

## 8. Risks and Mitigations

- Risk: API drift from domain rules.
  - Mitigation: centralize logic reuse and expand regression tests.
- Risk: mixed frontend stack complexity during transition.
  - Mitigation: strict phase gates and explicit decommission checklist.
- Risk: permissions bypass in new endpoints.
  - Mitigation: role tests for each staff/admin mutation path.
- Risk: inconsistent UX during partial migration.
  - Mitigation: route-level ownership and role-aware nav signals.

## 9. Implementation Backlog (Track Here)

### Active Tasks

- [x] Define and document migration architecture and cutover approach.
- [x] Add `/app` shell and SPA artifact pipeline.
- [x] Add customer API contracts (`auth`, `cafe`, `cowork`).
- [x] Add customer SPA views (`home`, `cafe`, `cowork`).
- [x] Add staff API contracts and SPA staff route.
- [x] Add role-specific navigation and guards in SPA.
- [x] Add browser smoke artifacts for migrated flows in `output/playwright/`.
- [x] Add account auth/profile APIs (`/api/auth/login|logout|register|profile`).
- [x] Add SPA account route and account UX (`/app/account`).
- [x] Prepare and implement root-route cutover with redirect map.
- [x] Decommission legacy frontend dependencies.

### Verification Checklist

- [x] `uv run pytest` passes.
- [x] `npm run build` passes.
- [x] Playwright smoke set captured for `/app` customer+staff routes.
- [x] Playwright smoke set captured for `/app/account`.
- [x] Feature-flagged route cutover tests pass.
- [x] Legacy-template dependency map completed.
- [ ] Final cutover sign-off approved.

## 10. Ownership and Update Policy

- Update this file at the end of each migration increment.
- Every completed feature must record:
  - affected endpoints/routes
  - tests added
  - rollback notes if behavior changed
- Treat this document as the single execution tracker for migration status.

## 11. Increment Log

### 2026-02-08 (Current Increment)

- Added staff API endpoints under `/api/cafe/staff/*` for:
  - active orders listing
  - status updates
  - payment toggles
  - menu availability toggles
  - customer lookup
- Added React `/app/staff` route with role-aware navigation and staff controls.
- Added and passed regression tests for staff API permission/mutation behaviors.
- Captured Playwright smoke screenshots:
  - `output/playwright/app-home.png`
  - `output/playwright/app-staff.png`
  - `output/playwright/app-staff-search.png`
- Added session/account API endpoints under `/api/auth/*` for:
  - login
  - logout
  - register (customer group assignment)
  - profile get/patch
- Added React `/app/account` route with:
  - SPA login/register forms for anonymous sessions
  - authenticated profile editing and logout
- Added and passed regression tests for account APIs:
  - `accounts/test_spa_api.py`
- Captured account smoke screenshots:
  - `output/playwright/app-account.png`
  - `output/playwright/app-account-anon.png`
- Added feature-flagged root route cutover controls:
  - setting: `DJANGO_SPA_PRIMARY` / `SPA_PRIMARY_ROUTES`
  - when enabled: root and non-system routes resolve to SPA shell
  - legacy views preserved under `/legacy/*`
  - compatibility redirects for `/login`, `/register`, `/profile`, `/cafe/*`, `/cowork/*`
- Added cutover regression tests:
  - `config/test_spa_cutover.py`
- Expanded migration regression suite across:
  - account auth/profile branches
  - cafe customer+staff edge cases
  - cowork validation and auth checks
  - cutover redirects + SPA catchall
- Decommission increment:
  - removed Alpine.js script include from `theme/templates/base.html`
  - replaced Alpine-based user dropdown behavior with vanilla JS in `theme/templates/base.html`
  - removed unused Alpine modal wrapper from `theme/templates/cowork/space_list.html`
  - added legacy dependency tracker: `LEGACY_FRONTEND_DEPENDENCY_MAP.md`
  - enabled `/legacy/*` route availability in default mode to support phased dependency isolation
  - added coverage for legacy route availability in default-mode cutover tests
  - moved jQuery + Persian datepicker includes from `theme/templates/base.html` to `theme/templates/cowork/book_space.html`
  - converted global price formatting helper in `theme/templates/base.html` to vanilla JS
  - added namespace-safe default legacy URL mirror module: `config/legacy_urls_default.py`
  - shifted default-mode `/cafe/*` and `/cowork/*` entry paths to redirects targeting `/legacy/*` routes
  - updated cutover tests to verify default-mode legacy redirects and `/legacy/*` reverse resolution
  - scoped HTMX CDN include in `theme/templates/base.html` to legacy routes only
  - extended cutover tests to assert HTMX script is absent on non-legacy pages and present on `/legacy/*` pages
  - scoped `hx-headers` and HTMX-specific listeners in `theme/templates/base.html` to `/legacy/*`
  - extended cutover tests to assert `hx-headers` is absent on non-legacy pages and present on `/legacy/*`
  - added server-side HTMX path guards in `cafe/views.py` and `cowork/views.py` so partial responses only render for `/legacy/*` requests
  - switched HTMX request detection from `request.htmx` middleware property to `HX-Request` header checks
  - removed `django_htmx` from runtime `INSTALLED_APPS` and `MIDDLEWARE` in `config/settings.py`
  - removed `django-htmx` from dependency manifests (`pyproject.toml`, `uv.lock`)
  - updated `item_quantity_control` partial to use explicit `is_htmx` context flag for OOB badge rendering
  - scoped React Bits CSS/JS includes and mount containers in `theme/templates/base.html` to `/legacy/*` only
  - added non-legacy static fallback UI for desktop quick-access and mobile bottom nav in `theme/templates/base.html`
  - expanded cutover assertions for legacy-only React Bits runtime includes (`config/test_spa_cutover.py`)
  - updated UI regression coverage for legacy-only React Bits mounts (`theme/test_ui.py`)
  - removed React Bits CSS/JS includes and legacy mount containers from `theme/templates/base.html`
  - removed legacy `data-rb-island` attributes from:
    - `theme/templates/home.html`
    - `theme/templates/cafe/menu.html`
    - `theme/templates/cowork/partials/zone_list.html`
  - removed React Bits static artifacts from `theme/static/js/` and removed React Bits build scripts from `theme/static_src/package.json`
  - removed jQuery + Persian datepicker includes and init script from `theme/templates/cowork/book_space.html`
  - switched legacy booking date input to plain validated `YYYY-MM-DD` text entry while keeping HTMX preview behavior
  - tightened CSP allowances by removing `code.jquery.com` and Persian datepicker stylesheet URL in `config/settings.py`
  - added legacy booking page regression assertion for removal of jQuery/Persian datepicker assets (`cowork/test_ui_ux.py`)
  - added `theme.context_processors.legacy_runtime_flags` and switched base-template HTMX/runtime guards to context flags instead of broad legacy-path checks
  - restricted HTMX script + `hx-headers` runtime to legacy routes with active `hx-*` behavior (`/legacy/cafe/menu|cart|dashboard` and `/legacy/cowork/` + `/legacy/cowork/book/*`)
  - expanded route cutover tests to assert legacy auth pages (`/legacy/login/`) do not load HTMX runtime
  - removed cowork HTMX polling/preview runtime:
    - `theme/templates/cowork/space_list.html` no longer uses periodic `hx-get` refresh
    - `theme/templates/cowork/book_space.html` no longer issues `hx-get` preview requests
    - `cowork/views.py` no longer serves HTMX partial branches
    - `theme/templates/cowork/partials/booking_preview.html` removed
  - tightened cutover assertions so `/legacy/cowork/` does not include HTMX runtime (`config/test_spa_cutover.py`)
  - updated cowork regression coverage for HX-header requests to render full templates (`cowork/test_cowork_logic.py`)
  - removed cafe customer HTMX runtime path:
    - `theme/templates/cafe/partials/item_quantity_control.html` now uses standard POST forms for `add_to_cart`/`remove_from_cart`
    - `theme/templates/cafe/partials/cart_list.html` now uses standard POST forms for quantity changes
    - `cafe/views.py` no longer returns customer HTMX partial branches for cart mutations/detail
    - `theme/context_processors.legacy_runtime_flags` updated prior to full HTMX decommission
  - removed final legacy HTMX runtime path:
    - `theme/templates/cafe/barista_dashboard.html` now uses standard POST actions and timed full-page refresh
    - `theme/templates/cafe/partials/order_list.html` no longer uses `hx-post` mutations
    - `cafe/views.py` no longer has HTMX-specific branches for dashboard/order mutations
    - removed temporary HTMX runtime context-processor wiring from `config/settings.py` and deleted `theme/context_processors.py`
- finalized SPA-first routing as always-on in URL configuration:
  - root and non-system routes resolve to SPA shell
  - compatibility redirects preserve `/login|/register|/profile`, `/cafe/*`, `/cowork/*`
  - obsolete `DJANGO_SPA_PRIMARY` / `SPA_PRIMARY_ROUTES` toggle removed from runtime settings
- removed legacy cafe/cowork public surface from routing:
  - `/legacy/cafe/*` now redirects to `/app/cafe`
  - `/legacy/cowork/*` now redirects to `/app/cowork`
  - removed unused `config/legacy_urls_default.py`
  - expanded cutover assertions so `/legacy/cafe/menu/` and `/legacy/cafe/dashboard/` both remain HTMX-free (`config/test_spa_cutover.py`)
  - updated cafe logic coverage for legacy HX-header cart mutations to redirect full-page (`cafe/test_cafe_logic.py`)
  - removed unused legacy partial templates:
    - `theme/templates/cafe/partials/cart_badge.html`
    - `theme/templates/cowork/partials/space_items.html`
  - updated UI assertions in `cafe/test_ui.py` and `cowork/test_ui_ux.py` for static card markup
  - added regression tests for HTMX isolation:
    - `cafe/test_cafe_logic.py` (customer + staff HTMX response branches)
    - `cowork/test_cowork_logic.py` (space list + booking preview HTMX branches)
- removed legacy account template entry routes from active UI surface:
  - `accounts:login|register|profile` now redirect to `/app/account`
  - `/legacy/login|register|profile` now redirect to `/app/account`
  - updated route regression assertions in `accounts/test_regression.py`, `theme/test_ui.py`, and `config/test_spa_cutover.py`
- removed dead legacy account auth/profile implementation:
  - deleted legacy templates: `theme/templates/registration/login.html`, `theme/templates/registration/register.html`, `theme/templates/accounts/profile.html`
  - removed unused template-backed view classes/functions from `accounts/views.py`
  - removed unused `CustomAuthenticationForm` from `accounts/forms.py`
- migrated auth-required redirect targets to SPA account:
  - `LOGIN_URL` now points directly to `/app/account`
  - session payload `login_url` now returns `/app/account`
  - updated auth redirect regression checks in `accounts/test_regression.py` and `accounts/test_rbac.py`
- moved template navigation auth/profile links to SPA-native account route:
  - updated `theme/templates/base.html` links to `/app/account` for login/register/profile entry points
- Latest validation results:
  - targeted migration tests: `34 passed`
  - full test suite: `109 passed`
  - re-verified full suite (post-regression expansion): `109 passed, 74 warnings`
  - post-decommission full suite re-verified: `109 passed, 74 warnings`
  - route-isolation increment full suite: `109 passed, 74 warnings`
  - post HTMX server-side isolation verification: `117 passed, 91 warnings`
  - post dependency/runtime isolation batch verification: `118 passed, 91 warnings`
  - post jQuery/datepicker removal verification: `119 passed, 92 warnings`
  - post selective HTMX runtime-gating verification: `119 passed, 92 warnings`
  - post cowork HTMX removal verification: `119 passed, 92 warnings`
  - post cafe customer HTMX removal verification: `119 passed, 92 warnings`
  - post full HTMX decommission verification: `119 passed, 92 warnings`
  - post legacy cafe/cowork hard-disable verification: `119 passed, 91 warnings`
  - post legacy account route redirect verification: `119 passed, 91 warnings`
  - post legacy account template cleanup verification: `119 passed, 91 warnings`
  - post SPA-native auth redirect target verification: `119 passed, 91 warnings`
  - post template nav SPA-account link verification: `119 passed, 91 warnings`

## 12. Handoff Snapshot

### Current Status

- Migration is stable at API + SPA layers for:
  - customer flows (`/app/cafe`, `/app/cowork`)
  - staff flows (`/app/staff`)
  - account flows (`/app/account`)
- Root cutover is now always-on SPA-first routing.

### Route Behavior

- Runtime mode:
  - root and non-system routes resolve to SPA shell.
  - `/legacy/cafe/*` and `/legacy/cowork/*` redirect to SPA.
  - `/legacy/login|register|profile` redirect to `/app/account`.
  - remaining `/legacy/*` usage is limited to transitional admin/logout routes.
  - compatibility redirects:
    - `/login|/register|/profile` -> `/app/account`
    - `/cafe/*` -> `/app/cafe`
    - `/cowork/*` -> `/app/cowork`
- Rollback strategy:
  - use checkpoint refs (branch/tag/commit) to restore pre-removal state if needed.

### Last Verified Commands

- `uv run pytest accounts/test_spa_api.py cafe/tests/test_spa_api.py cowork/test_spa_api.py config/test_spa_cutover.py -q`
- `uv run pytest -q`
- `cd theme/static_src && npm run build`
- `uv run python manage.py check`

### Rollback Reference

- Checkpoint commit: `d50872f`
- Checkpoint branch: `backup/legacy-ui-pre-removal`
- Checkpoint tag: `checkpoint/pre-legacy-removal-2026-02-08`

## 13. Context Recovery and Resume Checklist

Use this section first if chat history/context is truncated.

### Current Baseline (Trusted)

- Backend + SPA migration changes are applied and test-verified.
- Full suite currently passes (`119 passed`).
- SPA-first cutover is active and enforced in URL routing.

### Source of Truth Files

- Migration tracker: `REACT_MIGRATION_EXECUTION_PLAN.md`
- Legacy dependency map: `LEGACY_FRONTEND_DEPENDENCY_MAP.md`
- Cutover wiring: `config/urls.py`, `config/legacy_urls.py`
- API regression tests:
  - `accounts/test_spa_api.py`
  - `cafe/tests/test_spa_api.py`
  - `cowork/test_spa_api.py`
  - `config/test_spa_cutover.py`

### Resume Commands

- Backend tests:
  - `uv run pytest -q`
- Focused migration suite:
  - `uv run pytest accounts/test_spa_api.py cafe/tests/test_spa_api.py cowork/test_spa_api.py config/test_spa_cutover.py -q`
- Frontend production bundle:
  - `cd theme/static_src && npm run build`

### Next Implementation Focus (Ordered)

- Decommission remaining legacy admin/logout route dependencies under `/legacy/*` after parity sign-off.
- Remove redirect-only alias routes (`/login|/register|/profile`) when deep-link compatibility is no longer needed.
- Remove redirect-only named route aliases in `accounts.urls` once internal references are fully retired.
- Run full regression + smoke checks after each decommission batch.
