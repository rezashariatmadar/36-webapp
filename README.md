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
- `DJANGO_LOG_LEVEL` (default: `INFO`)
- `DJANGO_CSP` (Content Security Policy string)

**Tests**

```powershell
uv run pytest
```
