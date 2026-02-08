# UI/UX Audit Implementation Plan + Cleanup

Date: 2026-02-07
Scope: Implement fixes discovered via browser-driven UI/UX inspection and stabilize the working tree for safe delivery.

## 1. Goals

- Fix the highest-impact UI bugs discovered in login/register, cafe menu/cart, and React islands integration.
- Remove regressions in badge sync and cart currency rendering.
- Improve accessibility semantics for auth forms.
- Leave unrelated in-progress work untouched unless explicitly requested.

## 2. Confirmed Problems

1. HTMX actions inside React island cards are unreliable on first interaction.
- Root cause: HTMX processing is invoked immediately after `root.render(...)` in islands, before commit is guaranteed.
- Affected: `theme/static_src/src/reactbits/islands.js` (`mountPixelCard`, `mountSpotlightCard`).

2. Cart badge updates are inconsistent.
- Root cause: menu partial uses OOB id `cart-badge`, while base/nav sync expects `cart-badge-desktop` and `cart-badge-mobile`.
- Affected: `theme/templates/cafe/partials/item_quantity_control.html`, `theme/templates/base.html`.

3. Cart totals can display duplicated currency text.
- Root cause: JS `format-price` appends currency, while cart template also appends `تومان` next to formatted values.
- Affected: `theme/templates/cafe/partials/cart_list.html`, `theme/templates/base.html` formatting behavior.

4. Login/Register form accessibility issues.
- Root cause: labels are not semantically bound to inputs, and autocomplete attributes are missing on credential fields.
- Affected: `theme/templates/registration/login.html`, `theme/templates/registration/register.html`, `accounts/forms.py`.

## 3. Implementation Plan (Decision Complete)

### A. React islands + HTMX reliability

Files:
- `theme/static_src/src/reactbits/islands.js`

Changes:
- Add a helper that guarantees HTMX scans committed DOM after React render.
- Preferred approach: render synchronously (or post-render callback/microtask if strict sync is unavailable), then run `window.htmx.process(node)`.
- Apply this helper in both `mountPixelCard` and `mountSpotlightCard`.

Acceptance criteria:
- On `/cafe/menu/`, first click on `افزودن` immediately updates the control (button to +/-) with no manual `htmx.process` workaround.

### B. Badge sync contract unification

Files:
- `theme/templates/cafe/partials/item_quantity_control.html`
- `theme/templates/base.html` (only if needed for robust sync)

Changes:
- Replace OOB update id from `cart-badge` to `cart-badge-desktop` in menu item quantity partial.
- Ensure base sync script continues syncing desktop -> mobile badge reliably after HTMX swap.
- Keep IDs stable and unique.

Acceptance criteria:
- Add/remove from menu updates desktop badge and mobile badge in the same interaction cycle.
- Cart badge hides at zero and shows for positive count.

### C. Currency duplication fix

Files:
- `theme/templates/cafe/partials/cart_list.html`

Changes:
- Remove static currency label adjacent to values that already use `.format-price`.
- Keep formatter as single source of displayed currency suffix.

Acceptance criteria:
- Cart subtotal and total render with exactly one currency suffix.

### D. Auth form accessibility + autofill

Files:
- `theme/templates/registration/login.html`
- `theme/templates/registration/register.html`
- `accounts/forms.py`

Changes:
- Template labels:
  - Bind labels to fields: `<label for="{{ field.id_for_label }}">...</label>`.
- Form widgets:
  - Login username: `autocomplete="username"`.
  - Login password: `autocomplete="current-password"`.
  - Register password: `autocomplete="new-password"`.
  - Register confirm password: `autocomplete="new-password"`.
  - Register phone: `autocomplete="tel"` (or conservative phone-level token).
  - Preserve existing classes/placeholders.

Acceptance criteria:
- Browser no longer warns about missing autocomplete for auth credentials.
- Labels are programmatically associated with their inputs.

### E. Build and verify

Commands:
1. `cd theme/static_src && npm run build`
2. `uv run pytest accounts -k "normalization or nav or auth"` (targeted auth-facing checks)
3. Manual Playwright smoke pass:
- `/login/` and `/register/` field semantics check
- `/cafe/menu/` add/remove item
- `/cafe/cart/` badge + totals rendering

Acceptance criteria:
- Build passes.
- No regressions in auth flow and cart interactions.
- UI behavior matches fixed expectations above.

## 4. Cleanup Plan

## 4.1 Safety rules

- Do not reset or discard unrelated modified/deleted files unless explicitly requested.
- Keep cleanup narrowly scoped to artifacts and temporary outputs related to this implementation.

## 4.2 Cleanup tasks (scoped)

1. Remove transient Playwright artifacts generated during debugging that are not needed in version control.
- Candidate path: `output/playwright/` (retain only files explicitly requested by product/QA).

2. Ensure generated frontend outputs are intentional.
- If `theme/static/js/reactbits-islands.js` changes only due this fix, keep it.
- If unrelated generated noise appears, regenerate once from current source and keep deterministic output.

3. Leave pre-existing unrelated dirty files untouched.
- Existing modified/deleted files outside fix scope remain as-is.

4. Optional post-implementation hygiene (only when requested):
- Produce a dedicated commit containing only:
  - `theme/static_src/src/reactbits/islands.js`
  - `theme/templates/cafe/partials/item_quantity_control.html`
  - `theme/templates/cafe/partials/cart_list.html`
  - `theme/templates/registration/login.html`
  - `theme/templates/registration/register.html`
  - `accounts/forms.py`
  - `theme/static/js/reactbits-islands.js` (if regenerated)

## 5. Test Matrix

1. Menu HTMX lifecycle
- Given user opens `/cafe/menu/`
- When first click on `افزودن`
- Then quantity control switches immediately and badge increments.

2. Badge consistency
- Given cart count N
- When add/remove from menu and cart views
- Then `cart-badge-desktop` and `cart-badge-mobile` both reflect N.

3. Currency rendering
- Given cart with items
- Then subtotal/total show one `تومان` per formatted value.

4. Auth semantics
- Given `/login/` and `/register/`
- Then each visible field has associated label and expected autocomplete token.

## 6. Risks + Mitigations

- Risk: React render timing differences across environments.
- Mitigation: explicit post-render HTMX processing strategy with deterministic ordering.

- Risk: Badge script coupling to specific target id.
- Mitigation: preserve `cart-badge-desktop` as canonical OOB update id.

- Risk: Existing dirty worktree obscures review.
- Mitigation: keep implementation scoped and report changed files explicitly.

## 7. Deliverables

- Code fixes in scoped files listed above.
- Rebuilt `reactbits-islands` bundle if source changed.
- Validation evidence (commands run + observed outcomes).
- This plan/cleanup document.
