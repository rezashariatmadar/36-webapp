# Track Plan: Cafe Menu & Inventory

## Phase 1: Foundation & Modeling
- [x] Task: Create Cafe App & Models
    -   Define `MenuCategory` and `MenuItem`.
    -   Register models in Django admin.
- [x] Task: Data Import & Seeding
    -   Create management command `import_menu`.
    -   Import all items from `36 menu.csv`.

## Phase 2: User Interface
- [x] Task: Implement Public Menu View
    -   Create view with category grouping.
    -   Design minimalist, responsive template.
    -   Add link to main navbar.

## Phase 3: Order Management
- [x] Task: Create Order Models
    -   `CafeOrder`, `OrderItem`.
- [x] Task: Implement Barista Dashboard
    -   Real-time (polling) order queue.
- [x] Task: Customer Ordering Flow
    -   Shopping cart / checkout logic.
