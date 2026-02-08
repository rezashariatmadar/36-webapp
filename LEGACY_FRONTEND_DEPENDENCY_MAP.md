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
| HTMX | CDN script + Django middleware | active | Legacy template partial updates (cart/booking/staff polling) | `theme/templates/cafe/*`, `theme/templates/cowork/*`, `cafe/views.py`, `cowork/views.py`, `config/settings.py` | Remove after template routes are fully retired or isolated under `/legacy/*` only. |
| jQuery | CDN script | active | Required by current datepicker integration and shared formatter helper | `theme/templates/base.html` | Replace datepicker/format utilities with SPA or vanilla alternatives. |
| Persian Datepicker stack | CDN script/css | active | Jalali date input on legacy booking forms | `theme/templates/base.html`, `theme/templates/cowork/book_space.html` | Remove when booking UI is React-only. |
| React Bits Islands bundle | local static bundle | active (legacy-support) | Transitional visual islands in template pages | `theme/static_src/src/reactbits/*`, `theme/templates/base.html` | Remove after all legacy template pages are decommissioned. |

## Phase-Ordered Decommission Checklist

- [x] Remove Alpine.js runtime dependency from templates.
- [ ] Isolate HTMX-dependent routes to `/legacy/*` only.
- [ ] Remove jQuery-dependent datepicker glue in `theme/templates/base.html`.
- [ ] Remove `django-htmx` from `config/settings.py` and dependency manifests.
- [ ] Remove React Bits islands bundle from legacy base template.
- [ ] Prune unused template partials and legacy static JS.

## Validation Commands

- `uv run pytest config/test_spa_cutover.py -q`
- `uv run pytest cafe/tests/test_spa_api.py cowork/test_spa_api.py -q`
- `uv run pytest -q`
- `cd theme/static_src && npm run build`

## Notes

- Decommission work must not break `/legacy/*` fallback while `DJANGO_SPA_PRIMARY` remains optional.
- If a dependency is only used under `/legacy/*`, mark it as `active (legacy-only)` in future updates.
