Plan

Hard-Cutover Migration Plan: Django Theme Stack -> Full Vite React App in frontend/
Summary
This plan replaces the current Django template/theme frontend with a full React + Vite + TypeScript app in frontend/, with no legacy UI preservation.
Django remains backend-only for API + admin, and frontend is deployed separately but served under the same origin via proxy.

Locked Decisions
Frontend deployment: frontend/ app deployed separately.
Auth model: Django session + CSRF retained.
Network model: same-origin proxy (/api to Django).
Cutover style: hard cutover in one migration release.
Page scope: all non-admin pages ported.
URL strategy: preserve current public URLs.
Frontend language/tooling: React + TypeScript + Vite + npm.
Target Architecture
frontend/ is the only user-facing web app.
Django exposes only:
/api/auth/*
/api/cafe/*
/api/cowork/*
new /api/staff/* endpoints (defined below)
/admin/*
/media/* and /static/* (admin/static assets)
Reverse proxy routes:
/api/*, /admin/*, /media/*, /static/* -> Django
all other paths -> React index.html (SPA fallback)
Remove frontend rendering responsibility from Django (theme templates, HTMX, Alpine, jQuery, app shell, cutover flag logic).
Repository/Structure Changes
Add frontend/ Vite project (TypeScript):
frontend/src/assets
frontend/src/components
frontend/src/layouts
frontend/src/pages
frontend/src/features/account
frontend/src/features/cafe
frontend/src/features/cowork
frontend/src/features/staff
frontend/src/lib/api
frontend/src/lib/auth
frontend/src/styles
Move and adapt UI assets/styles from theme/static_src/src into frontend/src.
Do not keep Tailwind/DaisyUI as primary styling; preserve the visual language using React-first CSS and component patterns with Motion/Lucide/Excalidraw where applicable.
Remove legacy frontend sources after parity:
theme/templates/*
theme/static_src/*
reactbits-islands.*
spa-app.*
Backend cleanup:
remove theme from INSTALLED_APPS
remove django_htmx and tailwind app usage
remove SPA cutover routing (SPA_PRIMARY_ROUTES, app.html shell paths)
simplify CSP to remove inline/eval allowances previously needed by template scripts.
Route Migration Matrix (Preserved Public URLs)
Current URL	New React Page	Notes
/	HomePage	port home.html UI
/login/	LoginPage	API login
/register/	RegisterPage	API register
/profile/	ProfilePage	API profile get/patch
/cafe/menu/	CafeMenuPage	menu + add/remove cart
/cafe/cart/	CafeCartPage	cart detail/edit
/cafe/checkout/	CafeCheckoutPage	checkout submit
/cafe/orders/	CafeOrdersPage	history + reorder
/cowork/	CoworkSpacesPage	zones/spaces live state
/cowork/book/:spaceId	CoworkBookingPage	preview + create booking
/cowork/my-bookings/	CoworkMyBookingsPage	booking history
/cafe/dashboard/	StaffOrdersPage	active order ops
/cafe/manual-order/	StaffManualOrderPage	walk-in orders
/cafe/manage-menu/	StaffMenuStockPage	create/toggle menu items
/cafe/lookup/	StaffCustomerLookupPage	search customer
/cafe/analytics/	StaffAnalyticsPage	staff metrics
/staff/users/	StaffUsersPage	replacement for template user-admin screen
Public API / Interface Changes
Existing APIs remain and are reused:

/api/auth/*, /api/cafe/*, /api/cowork/* (current contracts stay stable).
Add these endpoints for full page parity:

GET /api/staff/analytics/overview/
returns cafe totals, today totals, top items, top buyers, cowork totals, occupancy, active bookings, top members.
GET /api/staff/users/
query: page, page_size, q, role, is_active
returns paginated user list with role flags.
PATCH /api/staff/users/{id}/status/
body: { "is_active": true|false }
PATCH /api/staff/users/{id}/role/
body: { "role": "Admin|Barista|Customer" }
GET /api/cafe/staff/menu-categories/
returns menu categories for create-item form.
POST /api/cafe/staff/menu-items/
supports creating menu item (name/description/price/category/is_available/image).
POST /api/cafe/staff/manual-orders/
body: customer identifier + item list + notes
creates paid walk-in order and returns created order summary.
Contract rules:

JSON-only responses.
permission checks server-side for every staff/admin mutation.
preserve detail and errors format style currently used.
Frontend Implementation Spec
Routing:
React Router with exact path parity from matrix above.
auth/role guards for staff routes.
Data layer:
fetch wrapper with credentials: "include".
CSRF header from cookie or /api/auth/me/ bootstrap token.
centralized error normalization.
State:
server state via query hooks per feature (menu, cart, bookings, staff).
local UI state per page.
Design portability:
port existing CSS tokens/classes first, then componentize.
preserve RTL (dir="rtl"), Persian typography, Jalali date UX.
Date handling:
React Jalali date picker component; submit backend-compatible YYYY-MM-DD.
Layout:
single AppShell with desktop sidebar + mobile bottom nav currently in base.html.
Remove script-era behavior:
replace Alpine/jQuery/HTMX behaviors with React hooks/components.
Cutover Sequence (Hard Cutover)
Build frontend/ scaffold and base shell.
Port shared styles/components and static assets.
Port customer pages and wire existing APIs.
Add missing staff/admin APIs and port staff pages.
Wire production proxy rules and Vite dev proxy.
Switch traffic to React for all non-admin routes.
Remove legacy Django template/theme frontend code.
Remove obsolete dependencies/config flags.
Update docs and run full regression.
Test Cases and Scenarios
Backend API tests:

Auth session lifecycle: me/login/register/logout/profile.
Cafe customer flow: menu/cart/checkout/orders/reorder.
Cowork flow: spaces/preview/book/my-bookings.
Staff order mutations: status/payment.
Staff inventory: create/toggle/list items and categories.
Staff manual order creation.
Staff analytics payload and permissions.
Staff users list/role/status permissions and validation.
Frontend tests:

Route rendering for all mapped URLs.
Auth guard behavior for staff-only pages.
Form validation and API error surfaces.
Cart and booking end-to-end page interactions.
E2E smoke (Playwright):

Anonymous browse -> login/register -> profile update.
Menu add/remove -> checkout -> orders.
Cowork preview -> booking -> my bookings.
Staff dashboard actions.
Manual order + menu stock + customer lookup + analytics.
Staff user role/status updates.
Build/check gates:

uv run pytest
cd frontend && npm run build
cd frontend && npm run test
Playwright smoke pass
Assumptions and Defaults
Proxy provides same-origin behavior in production; no cross-origin cookie mode needed.
Public URL parity is preserved except staff user-management route moved to /staff/users/.
Django admin remains only under /admin/.
Business logic stays in Django models/forms/services; React is presentation + orchestration.
No dual-run fallback after release; legacy template frontend is removed in this migration.
