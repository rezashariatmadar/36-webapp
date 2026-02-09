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

- Initial route JS payload target (gzip): `<= 180KB`.
- Hard cap requiring explicit approval: `250KB`.
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
4. Smoke check `/app`, `/app/account`, `/app/cafe`, `/app/cowork`, `/app/staff`
