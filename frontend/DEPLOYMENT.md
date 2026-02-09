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

## Caddy Skeleton (Option A)

```caddy
your.domain.tld {
  handle_path /api/* {
    reverse_proxy 127.0.0.1:8000
  }

  handle_path /admin/* {
    reverse_proxy 127.0.0.1:8000
  }

  handle /app/* {
    root * /var/www/36-webapp/frontend/dist
    try_files {path} /index.html
    file_server
  }
}
```

## CSRF Bootstrap Requirement

- After removing Django template fallback, SPA startup must initialize CSRF cookie before unsafe methods.
- Use `GET /api/auth/csrf/` at app boot.
- Confirm first `POST|PATCH|DELETE` works from cold SPA load without visiting Django HTML endpoints.

## Staging Validation Checklist

1. Deep-link fallback:
   - Open `/app/cafe`, `/app/cowork`, and `/app/staff` directly in a fresh browser tab.
   - Confirm the edge server returns SPA index fallback (no 404).
2. CSRF cold-start:
   - Open `/app/account` in a private window.
   - Confirm first unsafe call (login/register/profile mutation) returns app-level validation/auth responses, not CSRF 403.
3. Route ownership:
   - Confirm `/api/*` and `/admin/*` are served by Django upstream.
   - Confirm static SPA assets resolve under `/app/assets/*`.

## Rollback Strategy

- Keep Django Option-B SPA fallback for one release after Option-A deployment.
- If regressions appear, route traffic back to Option-B and fix forward in a new patch.
