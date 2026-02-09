# SPA Customization Guardrails

This project now treats `/app/*` as the only product UI surface.
To keep customization fast and safe, follow these rules for all new SPA work.

## 1. Ownership Boundary

- Django owns:
  - auth/session/csrf
  - `/api/*`
  - `/admin/*`
  - static/media delivery
- React SPA owns:
  - layout, visuals, interaction behavior, page composition
  - route UX under `/app/*`

## 2. Component Integration Rule

- Third-party visual kits (for example ReactBits) must be wrapped in local adapters first.
- Pages import adapters from local `ui` modules, not vendor components directly.
- Keep vendor-specific props hidden inside adapter components.

## 3. Theme Token Contract

- Use CSS variables in `app.css` for visual primitives:
  - color layers
  - surface colors
  - radius
  - blur/shadow
  - container sizing
- New themes should override variables, not rewrite page-level classes.

## 4. Performance Budgets

- Frozen baseline (2026-02-09 production build):
  - `theme/static/js/spa-app.js`: `138,334 B`
  - `theme/static/js/spa-app.css`: `950 B`
  - largest chunk: `theme/static/js/chunks/chunk-DZ4QUUKD.js` (`8,357 B`)
  - total JS chunks: `32,152 B`
- Enforced hard caps (`npm run check:spa-budgets`):
  - `spa-app.js` <= `150,000 B`
  - `spa-app.css` <= `2,000 B`
  - largest JS chunk <= `10,000 B`
  - total JS chunks <= `40,000 B`
- LCP target: `<= 2.5s` (desktop baseline).
- CLS target: `<= 0.1`.
- Heavy animation components must be lazy-loaded per route.

## 5. Accessibility and Motion

- Respect reduced-motion preferences for all non-essential animations.
- Keep semantic HTML and keyboard support in adapter components.
- Avoid motion-only communication of state.

## 6. Routing Policy

- Canonical UX routes are `/app/*` only.
- Retired compatibility paths (`/login|/register|/profile`, `/cafe/*`, `/cowork/*`) must not be reintroduced.

## 7. Validation Checklist (Every UI Batch)

1. `uv run pytest -q`
2. `uv run python manage.py check`
3. `cd theme/static_src && npm run build`
4. `cd theme/static_src && npm run check:spa-budgets`
5. Smoke check `/app`, `/app/account`, `/app/cafe`, `/app/cowork`, `/app/staff`
