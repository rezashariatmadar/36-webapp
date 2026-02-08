# 36-webapp

Django 5.2 web app with HTMX, DRF, and a Tailwind/PostCSS theme build.

**Requirements**
- Python 3.12+
- `uv` (Python package manager)
- Node.js (for the theme build)

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

**Theme (Tailwind/PostCSS)**
The theme build lives in `theme/static_src` and outputs CSS to `theme/static/css/dist/styles.css`.

1. Install Node deps:

```powershell
cd theme/static_src
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
