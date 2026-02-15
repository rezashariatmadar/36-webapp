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

**Docker Compose Development (hot reload)**
1. Create a dev env file:

```powershell
Copy-Item .env.docker.example .env.docker
```

2. Build and start services:

```powershell
docker compose --env-file .env.docker up --build
```

3. Enable file sync watch (hot reload without rebuilding):

```powershell
docker compose --env-file .env.docker watch
```

Note: this development stack builds `*-dev` images (`Dockerfile.dev` for frontend).  
Use production compose images for Docker Scout/security sign-off.

4. Endpoints:
- Frontend (Vite): `http://localhost:5173`
- Backend: `http://localhost:8000`
- Postgres: `localhost:5432`

5. Stop services:

```powershell
docker compose down
```

6. Reset volumes (DB/media/static):

```powershell
docker compose down -v
```

**Docker Compose Production-style run**
1. Create a prod env file:

```powershell
Copy-Item .env.docker.prod.example .env.docker.prod
```

2. Start with production compose file:

```powershell
docker compose -f compose.prod.yml --env-file .env.docker.prod up --build -d
```

For security refreshes (base image and OS package CVEs), force a fresh pull/rebuild:

```powershell
docker compose -f compose.prod.yml --env-file .env.docker.prod build --pull --no-cache
```

Scout target images after prod build:
- `36-webapp-webapp36-api:latest`
- `36-webapp-webapp36-web:latest`
- `36-webapp-postgres:latest` (custom wrapper over `POSTGRES_IMAGE` that removes `gosu`)

DB base can be switched via env for CVE comparison, for example:

```powershell
$env:POSTGRES_IMAGE="postgres:16.12-bookworm"
docker compose -f compose.prod.yml --env-file .env.docker.prod up -d db
```

**Environment Variables**
These are optional; defaults are defined in `config/settings.py`.

- `SECRET_KEY` (Liara default)
- `DJANGO_SECRET_KEY` (fallback compatibility key)
- `DJANGO_DEBUG` (default: `True`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (comma-separated)
- `DATABASE_URL` (recommended for production; Postgres connection URL)
- `POSTGRESQL_DB_HOST`, `POSTGRESQL_DB_PORT`, `POSTGRESQL_DB_NAME`, `POSTGRESQL_DB_USER`, `POSTGRESQL_DB_PASS` (Liara PostgreSQL-style variables; supported as fallback when `DATABASE_URL` is not set)
- `DJANGO_DB_SSL_REQUIRE` (set `True` if your database requires TLS)
- `DJANGO_SQLITE_PATH` (defaults to `db.sqlite3`)
- `DJANGO_LOG_LEVEL` (default: `INFO`)
- `DJANGO_CSP` (Content Security Policy string)

Production env template:
- `.env.example` (pre-filled for `36cowork.liara.run` and `webapp36-api.liara.run`)

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
- `frontend/liara_nginx.conf` (Liara React app)
- `deploy/nginx/react-django-cutover.conf` (self-managed nginx)

Cutover runbook:
- `docs/cutover-checklist.md`

Deployment runbook:
- `deploy/DEPLOYMENT.md`

Liara Docker deploy:
- Backend: `liara deploy` (run at repo root)
- Frontend: `cd frontend && liara deploy`

Pre-deploy validation scripts:
- Linux/macOS: `deploy/predeploy-check.sh`
- Windows PowerShell: `deploy/predeploy-check.ps1`

Example:
```powershell
powershell -ExecutionPolicy Bypass -File deploy/predeploy-check.ps1
```


