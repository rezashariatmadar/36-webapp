# Plan: UX/UI Polish & Component Standardization

## Phase 1: Foundation & Global Layers
- [x] Task: Define Design Tokens in `tailwind.config.js` and `styles.css` [345f6fe]
    - [x] Sub-task: Standardize colors (cyan, red, neutral), radii, and shadows in `tailwind.config.js`.
    - [x] Sub-task: Implement Typographic Scale (H1, H2, Body, Caption).
    - [x] Sub-task: Define `@layer components` for `.btn-primary`, `.btn-secondary`, `.btn-destructive`.
    - [x] Sub-task: Define `@layer components` for `.input-standard` and `.card-glass`.
- [x] Task: Implement Reusable Scrim Wrapper [345f6fe]
    - [x] Sub-task: Create a background wrapper class (with `::before`/`::after`) to apply the dark scrim consistently without breaking z-index.
- [x] Task: Implement Progressive Enhancement for Glass [345f6fe]
    - [x] Sub-task: Use `@supports` feature queries to detect `backdrop-filter` and `-webkit-backdrop-filter`.
    - [x] Sub-task: Configure fallback to increase background opacity while preserving borders/shadows when blur is missing.
- [x] Task: Conductor - User Manual Verification 'Foundation & Global Layers' (Protocol in workflow.md) [345f6fe]

## Phase 2: Navigation & Backend Context
- [x] Task: Implement Nav Context Processor [345f6fe]
    - [x] Sub-task: Create `accounts/context_processors.py` to return nav items based on static config and user role (No DB queries).
    - [x] Sub-task: Implement `is_active` logic using `request.resolver_match`.
    - [x] Sub-task: Register context processor in `settings.py`.
- [x] Task: Re-architect Global Navbar in `base.html` [345f6fe]
    - [x] Sub-task: Implement Right (Brand), Center (Nav), and Left (Actions/Account Dropdown) layout.
    - [x] Sub-task: Ensure keyboard operability for dropdowns.
- [x] Task: Implement Scrollable Category Tabs for Menu [345f6fe]
    - [x] Sub-task: Refactor category bar in `cafe/menu.html` into horizontal sticky tabs.

## Phase 3: Component Standardization & Partials
- [x] Task: Implement Numeral Normalization Logic [345f6fe]
    - [x] Sub-task: Create a utility function to normalize Persian/Latin digits to ASCII.
    - [x] Sub-task: Create a base form mixin to apply normalization in `clean` methods.
    - [x] Sub-task: Write unit tests for normalization utility and mixin.
- [x] Task: Standardize Form Inputs [345f6fe]
    - [x] Sub-task: Audit and apply `.input-standard` to all forms.
- [x] Task: Create Reusable UI Partials [345f6fe]
    - [x] Sub-task: Create `theme/templates/components/empty_state.html`.
    - [x] Sub-task: Create `theme/templates/components/kpi_card.html` (for dashboards).

## Phase 4: Page Polish & Accessibility Audit
- [x] Task: Refactor Home Page Density [345f6fe]
    - [x] Sub-task: Polish hero section and welcome blocks in `home.html`.
- [x] Task: Polish Coworking Discovery & Booking [345f6fe]
    - [x] Sub-task: Align actions in desk cards and standardize layout in `space_list.html`.
- [x] Task: Polish Cafe Menu & Cart [345f6fe]
    - [x] Sub-task: Improve action proximity (steppers) in menu lists.
    - [x] Sub-task: Implement standardized empty states for Cart and My Orders.
- [x] Task: Polish Admin & Data Views [345f6fe]
    - [x] Sub-task: Improve density and scanning in inventory tables.
    - [x] Sub-task: Refactor analytics dashboard with standardized KPI cards and layout.
- [x] Task: Focus & Non-Text Contrast Pass [345f6fe]
    - [x] Sub-task: Verify focus visibility (navbar, dropdowns, tabs, buttons, inputs).
    - [x] Sub-task: Verify focus/component contrast meets Non-Text Contrast (3:1).
    - [x] Sub-task: Ensure focus is not obscured by sticky headers.
- [x] Task: Final Accessibility & Contrast Audit [345f6fe]
    - [x] Sub-task: Verify text contrast meets WCAG targets (4.5:1 / 3:1).
- [x] Task: Conductor - User Manual Verification 'Page Polish & Accessibility Audit' (Protocol in workflow.md) [345f6fe]
