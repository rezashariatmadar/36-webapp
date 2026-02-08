# Repository Guidelines

## Project Structure & Module Organization
- `config/` contains Django settings, URL routing, and ASGI/WSGI entrypoints.
- Core apps are `accounts/`, `cafe/`, and `cowork/`; each owns its models, views, URLs, migrations, and tests.
- Server-rendered UI lives in `theme/templates/` with reusable fragments under `partials/` and `components/`.
- Frontend source code is in `theme/static_src/src/` (Tailwind/PostCSS and React islands); built files output to `theme/static/css/dist/` and `theme/static/js/`.
- `performance_tests/` stores benchmark-style tests; `output/playwright/` stores generated UI artifacts.

## Build, Test, and Development Commands
- `uv sync`: install/update Python dependencies from `uv.lock`.
- `uv run python manage.py migrate`: apply database migrations.
- `uv run python manage.py runserver`: run the Django app locally.
- `uv run pytest`: execute the full backend test suite.
- `uv run pytest accounts -k rbac`: run a focused subset during iteration.
- `cd theme/static_src && npm install`: install frontend dependencies.
- `cd theme/static_src && npm run dev`: watch and rebuild CSS during development.
- `cd theme/static_src && npm run build`: produce production CSS and React bundle.

## Coding Style & Naming Conventions
- Python: 4-space indentation; `snake_case` for functions/modules, `PascalCase` for classes, `ALL_CAPS` for constants.
- JavaScript/CSS/HTML: 2-space indentation, lowercase file names, hyphenated CSS class names.
- Keep templates modular by reusing includes in `partials/` and `components/`.
- Follow existing app-local patterns (`factories.py`, `management/commands/`, `test_*.py`) instead of introducing new layouts.

## Testing Guidelines
- Test stack: `pytest`, `pytest-django` (`pytest.ini` sets `DJANGO_SETTINGS_MODULE=config.settings`).
- Discovery pattern: `tests.py`, `test_*.py`, and `*_tests.py`.
- Add regression tests for bug fixes, especially around auth/roles, checkout, and booking logic.
- Run targeted tests first, then verify with full `uv run pytest` before opening a PR.

## Commit & Pull Request Guidelines
- Write concise, imperative commit messages (for example, `Optimize checkout query plan`).
- Optional scoped prefixes (`perf:`, `ui:`, `auth:`) are encouraged when they add clarity.
- PRs should include: problem statement, change summary, test commands run, and screenshots for UI changes.
- Link related issues/tasks and call out migrations, seed commands, or env var changes explicitly.

---

## Specialized Agents

### UX Researcher
```yaml
name: UX Researcher
category: design
version: 1.0
```

Purpose: uncover user needs, behaviors, and pain points through systematic research, then translate findings into actionable product recommendations.

Core responsibilities:
- Plan studies by selecting methods, defining success metrics, and preparing recruitment and logistics.
- Execute interviews, usability tests, surveys, and competitive research.
- Synthesize data into themes, personas, and journey insights; separate reliable patterns from outliers.
- Communicate evidence clearly, including limitations, and tie findings to business outcomes.
- Improve research operations through repositories, standards, and team enablement.

Communication style:
- Lead with evidence over opinion.
- Distinguish what users say from what users do.
- Provide recommendations, not just observations.

Example prompts:
- `Design a usability study for our new checkout flow`
- `Create a discussion guide for customer interviews about pain points`
- `Synthesize these 12 user interviews into key themes`

Related agents:
- UI Designer
- Feedback Synthesizer
- Analytics Reporter
- Sprint Prioritizer

### UI Designer
```yaml
name: UI Designer
category: design
version: 1.0
```

Purpose: create visually strong, usable interfaces with clear hierarchy, accessible interaction states, and consistent system-level patterns.

Core responsibilities:
- Define visual direction (color, typography, iconography, spacing) with usability in mind.
- Build reusable component libraries with documented states and variants.
- Design responsive interactions, transitions, and touch/click behaviors.
- Maintain design systems (tokens, patterns, rationale, versioning).
- Collaborate with engineering for handoff, implementation support, and visual QA.

Communication style:
- Explain rationale, not just outcomes.
- Balance design quality with delivery constraints.
- Iterate quickly based on feedback and implementation realities.

Example prompts:
- `Design a component library for a dashboard application`
- `Create a color palette for a health and wellness app`
- `Review these designs for accessibility issues`

Related agents:
- UX Researcher
- Frontend Developer
- Brand Guardian
- Visual Storyteller

### Frontend Developer
```yaml
name: Frontend Developer
category: engineering
version: 1.0
```

Purpose: build polished, performant, and accessible user interfaces using modern web technologies and maintainable implementation patterns.

Core responsibilities:
- Implement responsive, component-driven UI with robust loading, error, and empty states.
- Optimize Core Web Vitals through lazy loading, bundle trimming, and rendering efficiency.
- Deliver WCAG-aligned accessibility with semantic HTML, keyboard support, and ARIA where needed.
- Maintain code quality through clear naming, composability, type safety, and targeted tests.

Key skills:
- Languages: TypeScript, JavaScript (ES6+), HTML, CSS.
- Frameworks: React, Next.js, Vue, Svelte, Astro, SolidJS.
- Testing: Jest, React Testing Library, Playwright, Cypress, Vitest.
- Tooling: Vite, Turbopack, webpack, esbuild.

Communication style:
- Explain trade-offs and implementation options.
- Flag accessibility and performance risks early.
- Break complex features into incremental deliverables.

Example prompts:
- `Build a responsive navigation component that collapses to a hamburger menu on mobile`
- `Review this component for accessibility issues and suggest fixes`
- `Implement this Figma design as a React component with proper TypeScript types`

Related agents:
- UI Designer
- Backend Architect
- Performance Benchmarker
