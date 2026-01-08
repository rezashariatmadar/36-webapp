# Technology Stack - 36 Webapp

## Core Technologies
- **Programming Language:** Python
- **Backend Framework:** Django
- **Frontend Styling:** TailwindCSS
- **Frontend Interactivity:** HTMX (for polling and partial updates; no React)
- **Database:** SQLite (Development), PostgreSQL (Production)

## Key Technical Decisions
- **Localization:** 
    - **RTL:** Persian-first with global `dir="rtl"` and bidirectional text rendering support for mixed text.
    - **Calendar:** Jalali (Solar Hijri) for all displayed dates and inputs.
- **Architectural Principles:**
    - **Logic Separation:** Strict separation of concerns. Templates strictly for rendering; all business rules and logic reside in service functions.
    - **UI Pattern:** "Liquid Glass" - High-blur backdrop filters, translucent backgrounds, and animated SVG/CSS gradients for depth.
    - **Resource Model:** A unified "Resource" concept to manage seats, tables, and rooms, defined by their allowed booking modes.
- **Real-Time & Interactivity:**
    - **Polling:** Use HTMX `hx-trigger="every 5s"` (or 5-10s) for updating seat availability and the barista order queue.
    - **HTMX Patterns:**
        - `hx-get` for fetching availability fragments and lazy-loading hierarchical content (e.g., coworking zones).
        - `hx-post` for all booking and order actions.
- **Features & Status:**
    - **Seat Status:** 
        - **Green:** Available.
        - **Red:** Reserved (Must display "Reserved until [Jalali Datetime]").
    - **Payments:** Cash-only system. Use flags to track paid/unpaid status and record settlement timestamps.
