# Legacy Frontend Dependency Map

Date: 2026-02-08  
Scope: Track legacy frontend dependencies during Django-template to React migration.

## Status Legend

- `active`: still required by current code paths.
- `decommissioned`: removed from runtime template stack.
- `planned`: remove after route ownership cutover + parity checks.

## Dependency Inventory

| Dependency | Type | Current Status | Why It Exists | Primary Locations | Decommission Trigger |
| --- | --- | --- | --- | --- | --- |
| Alpine.js | CDN script | decommissioned | Previously used for dropdown/modal micro-state | `theme/templates/base.html`, `theme/templates/cowork/space_list.html` | Completed in this increment. |
| HTMX | CDN script | active (legacy-only selective runtime) | Legacy template partial updates (cart/booking/staff polling) | `theme/templates/cafe/*`, `theme/templates/cowork/*`, `cafe/views.py`, `cowork/views.py` | Remove after template routes are fully retired or isolated under `/legacy/*` only. |
| jQuery | CDN script | decommissioned | Previously used for legacy booking datepicker initialization | `theme/templates/cowork/book_space.html` | Completed in this increment. |
| Persian Datepicker stack | CDN script/css | decommissioned | Previously used for legacy booking date input picker | `theme/templates/cowork/book_space.html` | Completed in this increment. |
| React Bits Islands bundle | local static bundle | decommissioned (runtime removed) | Transitional visual islands previously used in template pages | `theme/static_src/src/reactbits/*` | Completed in this increment. |

## Phase-Ordered Decommission Checklist

- [x] Remove Alpine.js runtime dependency from templates.
- [x] Isolate HTMX-dependent routes to `/legacy/*` only.
- Progress note: default-mode `/cafe/*` and `/cowork/*` now redirect to `/legacy/*`, and primary reverse names resolve to `/legacy/*` for these apps.
- Progress note: HTMX CDN script is now loaded only when `request.path` is under `/legacy/*`, with cutover regression assertions.
- Progress note: `hx-headers` body attribute and HTMX-specific event listeners in base template are now bound only on `/legacy/*`.
- Progress note: HTMX runtime include and `hx-headers` are now further restricted to legacy routes with active `hx-*` interactions (cafe menu/cart/dashboard, cowork list/booking), while legacy auth pages do not load HTMX.
- Progress note: server-side HTMX partial rendering in `cafe/views.py` and `cowork/views.py` is now guarded by legacy path checks.
- [x] Remove jQuery-dependent datepicker glue in `theme/templates/base.html`.
- [x] Remove `django-htmx` runtime wiring from `config/settings.py`.
- [x] Remove `django-htmx` from dependency manifests.
- [x] Scope React Bits runtime includes in `theme/templates/base.html` to `/legacy/*`.
- [x] Remove React Bits islands bundle from legacy base template runtime.
- [x] Remove jQuery/Persian datepicker scripts from legacy booking template runtime.
- Progress note: `theme/templates/base.html` no longer includes React Bits CSS/JS and now uses static quick-access/mobile-nav markup across routes.
- Progress note: legacy `data-rb-island` attributes were removed from `theme/templates/home.html`, `theme/templates/cafe/menu.html`, and `theme/templates/cowork/partials/zone_list.html`.
- Progress note: generated React Bits static assets were removed from `theme/static/js/`, and React Bits build scripts were removed from `theme/static_src/package.json`.
- Progress note: `theme/templates/cowork/book_space.html` now uses a plain validated `YYYY-MM-DD` input with existing HTMX preview flow.
- [x] Prune unused template partials and legacy static JS.
- Progress note: removed orphaned legacy partials `theme/templates/cafe/partials/cart_badge.html` and `theme/templates/cowork/partials/space_items.html`; remaining `theme/static/js/*` assets are SPA runtime artifacts.

## Validation Commands

- `uv run pytest config/test_spa_cutover.py -q`
- `uv run pytest cafe/tests/test_spa_api.py cowork/test_spa_api.py -q`
- `uv run pytest -q`
- `cd theme/static_src && npm run build`

## Notes

- Decommission work must not break `/legacy/*` fallback while `DJANGO_SPA_PRIMARY` remains optional.
- If a dependency is only used under `/legacy/*`, mark it as `active (legacy-only)` in future updates.
- `/legacy/*` routes are now available in both default mode and SPA-primary mode to simplify phased isolation.
- Default-mode legacy mirror uses unique namespaces via `config/legacy_urls_default.py` to avoid URL namespace conflicts.
