# Frontend Deployment Runbook (`/app` Mount)

## Scope

- Frontend runtime is mounted at `/app/`.
- Django remains backend authority for `/api/*` and `/admin/*`.
- Auth model is Django session + CSRF.

## Local Development

1. Start backend:
   - `uv run python manage.py runserver 127.0.0.1:8000`
2. Start frontend:
   - `cd frontend && npm run dev`
3. Dev rules:
   - Use relative API paths only (`/api/...`).
   - Vite proxy forwards `/api/*` to `http://127.0.0.1:8000`.

## Build

- `cd frontend && npm run build`
- Output directory: `frontend/dist`

## Nginx Skeleton (Option A)

```nginx
upstream django_upstream {
  server 127.0.0.1:8000;
}

server {
  listen 80;
  server_name your.domain.tld;

  location /api/ {
    proxy_pass http://django_upstream;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /admin/ {
    proxy_pass http://django_upstream;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /app/ {
    alias /var/www/36-webapp/frontend/dist/;
    try_files $uri $uri/ /app/index.html;
  }
}
```

## CSRF Bootstrap Requirement

- After removing Django template fallback, SPA startup must initialize CSRF cookie before unsafe methods.
- Use `GET /api/auth/csrf/` at app boot.
- Confirm first `POST|PATCH|DELETE` works from cold SPA load without visiting Django HTML endpoints.

## Rollback Strategy

- Keep Django Option-B SPA fallback for one release after Option-A deployment.
- If regressions appear, route traffic back to Option-B and fix forward in a new patch.

