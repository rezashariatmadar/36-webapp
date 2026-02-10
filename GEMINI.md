# 36 Webapp - Context & Instructions

## Project Overview
**36 Webapp** is a unified platform for managing a coworking space and a cafe. It integrates seat and room reservations with a digital cafe ordering system, localized for Persian (RTL) and Jalali dates.

## Technology Stack
- Backend: Python, Django 5.x (API and admin)
- Frontend: React + TypeScript + Vite in `frontend/`
- UI libraries: `lucide-react`, `motion`, `@excalidraw/excalidraw`
- Localization: `django-jalali`, global `dir="rtl"`
- Testing: `pytest`, `vitest`, Playwright smoke

## Project Structure
| Directory | Purpose |
| :--- | :--- |
| `accounts/` | Authentication, profile, and staff user-management APIs |
| `cafe/` | Menu/cart/checkout/orders and staff cafe APIs |
| `cowork/` | Space discovery and booking APIs |
| `frontend/` | User-facing React app |
| `config/` | Django settings, middleware, and URL routing |

## Development Workflow

### Backend
```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
uv run pytest
cd frontend && npm run test
```

## Architecture Conventions
- Django serves backend concerns only: `/api/*`, `/admin/*`, `/media/*`, `/static/*`.
- React serves all non-admin user-facing pages.
- Session auth + CSRF are retained via same-origin API access.
- Legacy template/HTMX/Tailwind frontend is not part of target architecture.

## Important Files
- `README.md`: canonical setup instructions
- `plan.md`: hard-cutover migration plan
- `frontend/src/App.tsx`: route mapping and guards
- `frontend/vite.config.ts`: dev proxy settings
- `config/urls.py`: backend-only route map
