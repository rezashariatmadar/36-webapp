# 36-webapp

Django 5.2 backend (API/admin) with a separate Vite React frontend in `frontend/`.

**Requirements**
- Python 3.12+
- `uv` (Python package manager)
- Node.js (for the React frontend)

**Quick Start**
1. Install Python deps:

```powershell
uv sync
```

2. Run migrations:

```powershell
uv run python manage.py migrate
```

3. Start the Django server:

```powershell
uv run python manage.py runserver
```

**Frontend (Vite React)**
The frontend app lives in `frontend/` and is served separately. In development, use Vite dev server with API proxy.

1. Install Node deps:

```powershell
cd frontend
npm install
```

2. Watch for changes:

```powershell
npm run dev
```

3. Build for production:

```powershell
npm run build
```

**Environment Variables**
These are optional; defaults are defined in `config/settings.py`.

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (default: `True`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (comma-separated)
- `DJANGO_SQLITE_PATH` (defaults to `db.sqlite3`)
- `DJANGO_LOG_LEVEL` (default: `INFO`)
- `DJANGO_CSP` (Content Security Policy string)

Production env template:
- `.env.example`

**Tests**

```powershell
uv run pytest
```

```powershell
cd frontend
npm run test
```

## New APIs: Blog + Freelancers

- `GET /api/blog/posts/`
- `GET /api/blog/posts/{slug}/`
- `GET /api/blog/tags/`
- `GET /api/freelancers/`
- `GET /api/freelancers/{slug}/`
- `GET /api/freelancers/specialties/`
- `GET /api/freelancers/flairs/`
- `GET /api/auth/freelancer-profile/`
- `PATCH /api/auth/freelancer-profile/`
- `POST /api/auth/freelancer-profile/submit/`
- `GET /api/auth/freelancer-specialties/`
- `GET /api/auth/freelancer-flairs/`
- `POST /api/auth/freelancer-services/`
- `PATCH /api/auth/freelancer-services/{id}/`
- `DELETE /api/auth/freelancer-services/{id}/`

## SEO Endpoints

- `GET /sitemap.xml`
- `GET /robots.txt`

## Seed Freelancer Taxonomy

```powershell
uv run python manage.py seed_freelancer_taxonomy
```

## Production Proxy (Same Origin)

Use a same-origin reverse proxy so browser session/CSRF behavior stays consistent:
- `/api/*`, `/admin/*`, `/media/*`, `/static/*` -> Django
- all other paths -> React `index.html` (SPA fallback)

Reference config:
- `deploy/nginx/react-django-cutover.conf`

Cutover runbook:
- `docs/cutover-checklist.md`

Deployment runbook:
- `deploy/DEPLOYMENT.md`
- `deploy/VERCEL_RENDER_ALPHA.md` (Vercel frontend + Render backend)

Pre-deploy validation scripts:
- Linux/macOS: `deploy/predeploy-check.sh`
- Windows PowerShell: `deploy/predeploy-check.ps1`

Example:
```powershell
powershell -ExecutionPolicy Bypass -File deploy/predeploy-check.ps1
```
