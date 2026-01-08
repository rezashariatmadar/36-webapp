# Specification: UX/UI Polish & Component Standardization

## 1. Overview
Refactor the application's user interface to improve clarity, hierarchy, and accessibility while establishing a consistent "Liquid Glass" design system. This track focuses on re-architecting the navigation, standardizing typography and components (buttons, inputs, empty states), and ensuring WCAG-compliant contrast and RTL consistency.

## 2. Functional Requirements

### 2.1. Navigation Re-architecture
- **Global Navbar (base.html):**
    - **Right (Brand):** Compact "۳۶" wordmark, clickable to home.
    - **Center (Nav):** Primary links (3-5 items) injected via context processor.
        - **Logic:** Context processor returns a list of items (`label`, `url_name`, `roles`, `is_active`). `is_active` computed via `request.resolver_match`.
    - **Left (Actions):** Account dropdown (avatar + name/phone), cart icon with badge, and admin panel access moved into the dropdown.
- **Menu Category Bar:** Transform into horizontal scrollable sticky tabs under the navbar. Highlight the active category. Ensure keyboard operability.

### 2.2. Design System & Component Standardization
- **Implementation Strategy:**
    - **Styling:** Defined via Tailwind `@layer components` in `styles.css` for abstractions like `.btn`, `.card`.
    - **Structure:** Reusable Django partials for complex blocks (Empty States, KPI Cards, Navbar Actions).
- **Standardized Components:**
    - **Buttons:** Canonical `btn-primary` (Accent Cyan), `btn-secondary` (Outline/Neutral), and `btn-destructive` (Red). Consistent hover/focus states.
    - **Inputs:** Uniform height (44-48px) and padding. Consistent label and helper text placement. Validated error states (border + text + icon).
    - **Empty States:** Pattern: [Icon] -> [Headline] -> [1-line Description] -> [Primary/Secondary CTAs].
- **Typography:**
    - Scale: H1 (32-36px), H2 (20-24px), Body (14-16px), Caption (12-13px).
    - **Numerals Strategy:** 
        - **Display:** Render Persian digits for prices, counts, and non-technical text.
        - **Input:** Accept both Persian and Latin digits; normalize to ASCII digits for backend validation and storage.
        - **Normalization Scope:** Applies to National ID, Phone, Quantities, Admin Prices, and Search.
    - Localization: Replace all remaining English strings (e.g., "Full name", "Birth date") with Persian equivalents.

### 2.3. Layout, Density & Readability
- **Container:** Standardized max-width (1200px) with 12-column responsive grid.
- **Spacing:** Implement an 8px vertical rhythm.
- **Readability Enhancements:**
    - **Background Scrim:** Add a global 40-60% dark overlay over the background image.
    - **Glass Refinement:** Increase `.glass-panel` opacity for data-heavy screens.
    - **Cross-Browser & Fallback:** 
        - Use `@supports` feature queries to detect `backdrop-filter` (and `-webkit-backdrop-filter`).
        - Fallback: Increase background opacity while preserving structure (border/shadow) if blur is unsupported.
- **Proximity:** Align actions (steppers, buttons) closer to the objects they control.

## 3. Acceptance Criteria (Definition of Done)

- **Accessibility:**
    - [ ] **Text Contrast:** >= 4.5:1 for normal text; >= 3:1 for large-scale text.
    - [ ] **Non-Text Contrast:** >= 3:1 for UI components, borders, icons, and focus rings.
    - [ ] **Focus Visibility:** Focus indicator has >= 3:1 contrast against adjacent colors and is not obscured.

- **Navigation:**
    - [ ] Role-based items render correctly via context processor.
    - [ ] Active state is visually distinct and computed correctly.
    - [ ] Dropdowns and tabs are keyboard accessible.
    - [ ] Cart badge is present and accurate.

- **Components:**
    - [ ] **Buttons:** Consistent sizes; defined hover/active/disabled/focus states; destructive variant used appropriately.
    - [ ] **Inputs:** Label/helper placement consistent; error state consistent; focus state passes contrast.
    - [ ] **Empty States:** Follow specified pattern; include at least 1 primary CTA; consistent icon sizing.

- **Numerals:**
    - [ ] Backend normalizes Persian/Latin input to ASCII for specified fields.
    - [ ] Frontend displays Persian digits in specified contexts.

## 4. Technical Constraints
- **Framework:** Django Templates + Tailwind CSS + HTMX.
- **Style Guide:** Google Python Style Guide for backend; logical properties for CSS (e.g., `padding-inline-start`).
