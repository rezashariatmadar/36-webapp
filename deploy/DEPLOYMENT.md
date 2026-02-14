# Deployment Guide (Alpha)

For managed hosting split across Vercel (frontend) + Render (backend), use:
- `deploy/VERCEL_RENDER_ALPHA.md`

This repo is deployed as:
- Django backend for `/api/*`, `/admin/*`, `/media/*`, `/static/*`, `/sitemap.xml`, `/robots.txt`
- React SPA bundle for all other routes

Nginx reference config:
- `deploy/nginx/react-django-cutover.conf`

## 1) Server prerequisites
- Linux host with `nginx`
- Python 3.12+
- `uv`
- Node.js 20+ and npm

## 2) Pull code and configure env
1. Clone/pull this repo on server.
2. Create a production env file from `.env.example`.
3. Export env vars before starting Django (or load via systemd environment file).

Minimum required values:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

Example:
```bash
export DJANGO_SECRET_KEY='replace-me-with-random-secret'
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS='example.com,www.example.com'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://example.com,https://www.example.com'
```

## 3) Build backend
```bash
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
```

Optional initial data seed (new environments):
```bash
uv run python manage.py init_roles
uv run python manage.py import_menu --file "36 menu.csv"
uv run python manage.py seed_spaces
uv run python manage.py seed_freelancer_taxonomy
```

## 4) Build frontend
```bash
cd frontend
npm ci
npm run build
```

Expected output:
- `frontend/dist`

## 5) Configure application process
Run Django behind a process manager on `127.0.0.1:8000`.

Example (replace with your preferred process manager):
```bash
uv run python manage.py runserver 127.0.0.1:8000
```

For production reliability, use a supervised process (systemd/supervisor/container entrypoint).

## 6) Configure Nginx
1. Copy `deploy/nginx/react-django-cutover.conf` to your nginx site config.
2. Verify paths:
   - `root /var/www/36-webapp/frontend/dist;`
   - `upstream django_backend` points to your Django process (`127.0.0.1:8000`)
3. Validate and reload:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 7) Post-deploy verification
Run smoke checks:
- `/`
- `/login/`
- `/register/`
- `/cafe/menu/`
- `/cowork/`
- `/profile/`
- `/cafe/dashboard/` (staff)
- `/cafe/manual-order/` (staff)
- `/sitemap.xml`
- `/robots.txt`

API checks:
- `/api/auth/me/`
- `/api/cafe/menu/`
- `/api/cowork/spaces/`

## 8) Rollback
1. Switch nginx root/proxy back to previous release.
2. Restart/reload services.
3. Re-run smoke checks.

## 9) Release gates (must pass before deploy)
```bash
./deploy/predeploy-check.sh
```

PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File deploy/predeploy-check.ps1
```

Notes:
- Scripts run backend tests in test-safe mode (`DJANGO_DEBUG=True`) to avoid HTTPS redirect side effects in Django test client.
- Scripts run deploy security validation with `DJANGO_DEBUG=False` and fail on any deploy warning.
