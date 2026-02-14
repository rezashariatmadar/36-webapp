# Vercel + Render Alpha Release

This runbook deploys:
- Frontend (Vite React) on Vercel
- Backend (Django API/admin) on Render

## 1) Render backend setup
1. In Render, create a new **Blueprint** service from this repo (uses `render.yaml`).
2. Replace placeholders in `render.yaml`:
   - `<your-render-service>`
   - `<your-vercel-domain>`
3. Keep disk enabled (`/var/data`) so SQLite survives deploys/restarts.
4. Deploy.

Notes:
- Prefer setting `DATABASE_URL` to managed Postgres for production reliability.
- `DJANGO_SQLITE_PATH=/var/data/db.sqlite3` remains as fallback for alpha-only setups.

## 2) Seed initial data on Render
Run these from Render Shell (once on first environment):

```bash
uv run python manage.py init_roles
uv run python manage.py import_menu --file "36 menu.csv"
uv run python manage.py seed_spaces
uv run python manage.py seed_freelancer_taxonomy
```

## 3) Vercel frontend setup
1. Create a Vercel project with **Root Directory = `frontend`**.
2. Build settings:
   - Install: `npm ci`
   - Build: `npm run build`
   - Output: `dist`
3. In `frontend/vercel.json`, replace `<your-render-service>`.
4. Deploy.

`frontend/vercel.json` proxies backend routes to Render and keeps SPA route fallback working.

## 4) Required domain/env alignment
Backend env vars must include exact deployed domains:
- `DJANGO_ALLOWED_HOSTS=<render-host>,<vercel-host>`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://<render-host>,https://<vercel-host>`
- `DATABASE_URL=<postgres-connection-url>` (recommended)

If Vercel creates a new preview domain, add it before testing auth forms.

## 5) Smoke test checklist
After both deploys:
- `/`
- `/login/`
- `/register/`
- `/cafe/menu/`
- `/cowork/`
- `/profile/` (after login)
- `/admin/`
- `/api/auth/me/`
- `/api/cafe/menu/`
- `/api/cowork/spaces/`
- `/sitemap.xml`
- `/robots.txt`

## 6) Known alpha constraints
- SQLite on a mounted disk is acceptable for alpha, but migrate to managed Postgres before beta.
