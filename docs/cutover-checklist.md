# Hard Cutover Checklist (Django API/Admin + React Frontend)

## Architecture
- Django serves only `/api/*`, `/admin/*`, `/media/*`, `/static/*`.
- React SPA handles all user-facing routes with fallback to `index.html`.
- Same-origin proxy is required in production (see `deploy/nginx/react-django-cutover.conf`).

## Pre-Cutover Validation
1. Backend tests:
   - `uv run pytest`
2. Frontend build:
   - `cd frontend && npm run build`
3. Frontend tests:
   - `cd frontend && npm run test`
4. Playwright smoke evidence:
   - Route screenshots in `output/playwright/`
   - Route snapshots in `output/playwright/`
   - Smoke report summary in `output/playwright/smoke-report-2026-02-12.md`

## Required Route Parity
- `/`
- `/login/`
- `/register/`
- `/profile/`
- `/cafe/menu/`
- `/cafe/cart/`
- `/cafe/checkout/`
- `/cafe/orders/`
- `/cowork/`
- `/cowork/book/:spaceId`
- `/cowork/my-bookings/`
- `/cafe/dashboard/`
- `/cafe/manual-order/`
- `/cafe/manage-menu/`
- `/cafe/lookup/`
- `/cafe/analytics/`
- `/staff/users/`

## Access Control Expectations
- Unauthenticated access to protected customer routes redirects to `/login/`.
- Non-staff access to staff routes redirects to `/login/`.

## Rollback
1. Switch ingress/proxy back to prior frontend deployment.
2. Keep Django API/admin unchanged (no rollback needed for API-only URLs).
3. Re-run smoke checks against restored frontend.
