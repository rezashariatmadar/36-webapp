# Track Plan: UX Polish & Cowork Hierarchical View

## Phase 1: Navbar & Layout Fixes
- [x] Task: Refactor Navbar to Split Layout 6cac771
    -   Logo to the far right.
    -   Navigation links ("Menu", "Reserve") to the center.
    -   Profile dropdown to the far left.
- [x] Task: Fix Profile Dropdown Alignment & Clipping 6cac771
    -   Ensure the dropdown menu is fully visible in RTL mode.
    -   Fix overlap with main content.
- [~] Task: Conductor - User Manual Verification 'Navbar & Layout Fixes' (Protocol in workflow.md)

## Phase 2: Cafe Ordering Enhancements
- [x] Task: Style "Add to Cart" Buttons for High Contrast 5035bb4
    -   Update `cafe/menu.html` to use a bright secondary color for the (+) buttons.
- [x] Task: Implement Bottom-Left Floating Cart Indicator 5035bb4
    -   Create a sticky/floating component at the bottom left.
    -   Display real-time (HTMX-ready) cart count.
- [~] Task: Conductor - User Manual Verification 'Cafe Ordering Enhancements' (Protocol in workflow.md)

## Phase 3: Coworking Hierarchical UX
- [x] Task: Create Category-based Space Views c091c1f
    -   Modify `cowork/views.py` to support fetching spaces by `ZoneType`.
- [x] Task: Implement HTMX Hierarchical List c091c1f
    -   Update `cowork/space_list.html` to display category headers.
    -   Add `hx-get` to headers to lazy-load available seats on click.
- [~] Task: Conductor - User Manual Verification 'Coworking Hierarchical UX' (Protocol in workflow.md)

## Phase 4: Final Polish
- [x] Task: Mobile & RTL Responsive Audit
    -   Verify the split navbar and floating cart on mobile devices.
- [ ] Task: Final Localization & RTL Audit
    -   Ensure all labels are Persian and layouts are consistent.
- [x] Task: Conductor - User Manual Verification 'Final Polish' (Protocol in workflow.md)
