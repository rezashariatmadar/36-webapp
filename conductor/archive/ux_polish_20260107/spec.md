# Track Specification: UX Polish & Cowork Hierarchical View

## Overview
This track aims to resolve alignment issues in the navbar, improve the visibility of ordering actions in the cafe menu, and introduce a more structured, lazy-loaded list for coworking space reservations.

## Functional Requirements
### 1. Navbar Redesign (RTL Split)
- **Structure**:
    - Right: Logo ("۳۶").
    - Middle: Navigation links ("منو", "رزرو فضا").
    - Left: User profile dropdown.
- **Fix**: Resolve the overlapping and cut-off issues seen in the profile dropdown.

### 2. Cafe Menu UI Improvements
- **"Add to Cart" Button**: Update the style to use the project's secondary color (brighter contrast) to ensure visibility on dark cards.
- **Cart Indicator**: Implement a floating action button (FAB) or sticky bar at the **bottom left** of the viewport. It must display the current cart count and link to the cart detail page.

### 3. Coworking Hierarchical View
- **Categories**: Group spaces by `ZoneType` (Communal Table, Desk, etc.).
- **Interaction**: Users see a list of categories. Clicking a category expands it.
- **HTMX Lazy Loading**: The list of seats within a category is fetched and rendered only when the category is expanded.
- **Status**: Display seat names and availability status clearly.

## Technical Requirements
- **HTMX**: Use for expanding coworking categories and potentially updating the cart count.
- **Tailwind CSS**: Use DaisyUI components and standard Tailwind utilities for the split navbar and floating cart.
- **RTL**: Ensure all spacing and alignments (e.g., `left-0` vs `right-0`) are correctly handled for the Persian interface.

## Acceptance Criteria
- [ ] Navbar logo is far right, links are centered, and profile is far left.
- [ ] Profile dropdown content is fully visible and correctly aligned.
- [ ] "Add to Cart" buttons on the menu are high-contrast and easily clickable.
- [ ] A cart count indicator is visible at the bottom left of the screen.
- [ ] Coworking categories expand to show seats via HTMX.
