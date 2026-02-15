# Deployment Guide (Liara)

This repository is configured for a two-app Liara deployment:
- Django app (root): serves backend routes (`/api/*`, `/admin/*`, `/media/*`, `/static/*`, `/sitemap.xml`, `/robots.txt`)
- React app (`frontend/`): serves SPA routes and proxies backend paths to Django
- Both apps deploy via Docker (`platform: docker`)

Official references:
- https://docs.liara.ir/paas/django/quick-start/
- https://docs.liara.ir/paas/django/how-tos/create-app/

## 1) Deploy Django app (root)
1. In Liara dashboard, create a Docker app for backend.
2. `liara.json` is already set for backend app id `webapp36-api`.
3. Configure env vars from `.env.example`:
- `SECRET_KEY` (Liara default)
- `DJANGO_SECRET_KEY` (fallback compatibility key)
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=<frontend-domain>,<backend-domain>`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://<frontend-domain>,https://<backend-domain>`
- `DATABASE_URL` (recommended) or `POSTGRESQL_DB_*`
4. Deploy from the repository root with:
```bash
liara deploy
```
5. Backend Docker startup runs:
- `python manage.py migrate --noinput`
- `python manage.py collectstatic --noinput`
- `gunicorn config.wsgi:application --bind 0.0.0.0:8000 ...`

Optional first-time seed commands:
```bash
python manage.py init_roles
python manage.py import_menu --file "36 menu.csv"
python manage.py seed_spaces
python manage.py seed_freelancer_taxonomy
```

## 2) Deploy React app (`frontend/`)
1. In Liara dashboard, create a Docker app for frontend.
2. `frontend/liara.json` is already set for frontend app id `36cowork`.
3. `frontend/liara_nginx.conf` is configured for private network host `webapp36-api:8000`.
4. Deploy from `frontend/` directory with:
```bash
liara deploy
```

Notes:
- Frontend build output is `frontend/build` (configured in `frontend/vite.config.ts`).
- `frontend/liara_nginx.conf` keeps same-origin browser behavior by proxying backend paths through the frontend domain.

## 3) Post-deploy verification
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

## 4) Release gates (must pass before deploy)
```bash
./deploy/predeploy-check.sh
```

PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File deploy/predeploy-check.ps1
```


## 5) Private network requirement
- Put webapp36-api, 36cowork, and PostgreSQL in the same private network.
- Private network cannot be changed after app creation; recreate app if needed.

