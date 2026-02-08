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
- Feature-flagged root cutover routing implemented via `DJANGO_SPA_PRIMARY`.
- Legacy route fallback path added under `/legacy/*` for safe rollback operations.
- Legacy route namespace (`/legacy/*`) now available in both default mode and SPA-primary mode.
- Expanded regression coverage for migration APIs and cutover behavior; full suite currently green.
- Alpine.js template directives and CDN dependency removed from runtime templates.
- jQuery/Persian datepicker assets removed from global base template and scoped to legacy booking form only.
- Default-mode `/cafe/*` and `/cowork/*` now redirect into `/legacy/*` ownership.
- HTMX script loading is scoped to `/legacy/*` template responses only.
- HTMX body headers/event listeners in base template are scoped to `/legacy/*` only.

### In Progress

- Legacy dependency decommission execution (HTMX/jQuery/template pruning).
- Expanded SPA navigation and role-aware surfaces.

### Not Started

- Root (`/`) cutover to SPA.
- Decommission of legacy template/HTMX/jQuery paths.

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

- Keep template routes and existing views operational until cutover sign-off.
- Introduce new APIs/routes additively; avoid destructive route rewrites mid-phase.
- If regressions occur, route users back to template endpoints while preserving migrated code for patching.

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
- [x] Prepare and implement root-route cutover with redirect map (feature-flagged).
- [ ] Decommission legacy frontend dependencies.

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
- Latest validation results:
  - targeted migration tests: `34 passed`
  - full test suite: `109 passed`
  - re-verified full suite (post-regression expansion): `109 passed, 74 warnings`
  - post-decommission full suite re-verified: `109 passed, 74 warnings`
  - route-isolation increment full suite: `109 passed, 74 warnings`

## 12. Handoff Snapshot

### Current Status

- Migration is stable at API + SPA layers for:
  - customer flows (`/app/cafe`, `/app/cowork`)
  - staff flows (`/app/staff`)
  - account flows (`/app/account`)
- Root cutover is implemented but controlled by feature flag.

### Flag and Route Behavior

- Default mode (`DJANGO_SPA_PRIMARY=false`):
  - legacy routes remain primary.
- Cutover mode (`DJANGO_SPA_PRIMARY=true`):
  - root and non-system routes resolve to SPA shell.
  - legacy pages remain reachable under `/legacy/*`.
  - compatibility redirects:
    - `/login|/register|/profile` -> `/app/account`
    - `/cafe/*` -> `/app/cafe`
    - `/cowork/*` -> `/app/cowork`

### Last Verified Commands

- `uv run pytest accounts/test_spa_api.py cafe/tests/test_spa_api.py cowork/test_spa_api.py config/test_spa_cutover.py -q`
- `uv run pytest -q`
- `cd theme/static_src && npm run build`
- `uv run python manage.py check`

### Rollback Reference

- Checkpoint commit: `9f4f7f6`
- Checkpoint tag: `rollback/checkpoint-2026-02-08-react-migration`

## 13. Context Recovery and Resume Checklist

Use this section first if chat history/context is truncated.

### Current Baseline (Trusted)

- Backend + SPA migration changes are applied and test-verified.
- Full suite currently passes (`109 passed`).
- Cutover remains feature-flagged (`DJANGO_SPA_PRIMARY`) and is not forced on by default.

### Source of Truth Files

- Migration tracker: `REACT_MIGRATION_EXECUTION_PLAN.md`
- Legacy dependency map: `LEGACY_FRONTEND_DEPENDENCY_MAP.md`
- Cutover wiring: `config/settings.py`, `config/urls.py`, `config/legacy_urls.py`
- Default-mode legacy mirror: `config/legacy_urls_default.py`
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

- Decommission unused HTMX/jQuery/template fragments behind the migration.
- Run full regression + smoke checks after each decommission batch.
- Move `DJANGO_SPA_PRIMARY` from opt-in to default-on only after decommission sign-off.
