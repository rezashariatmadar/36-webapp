# Mobile Delivery Plan

**Context**
- Repo: Django 5.2 (HTMX/Tailwind, DRF), SQLite dev DB, initial code complete. Target date: January 27, 2026.
- Targets: PWA (web), Direct Android APK download (GitHub Releases).
- Guiding principles: one backend, shared design tokens, GitHub-first distribution, security-by-default.

## Phase 0 – Foundations (week 1: Jan 27–Jan 31, 2026)
**Goal:** Production-ready infrastructure and security baseline.

- **Environment & DB:**
    - Move from SQLite to **PostgreSQL 16+** (use `docker-compose` for local dev).
    - Implement `python-decouple` to load configuration from `.env`.
    - Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` (critical for PWA/Capacitor).
- **Security Hardening:**
    - **CORS:** Install `django-cors-headers`. Whitelist PWA/App origins.
    - **CSP:** Install `django-csp`. Define strict policy (e.g., `script-src 'self'`, `connect-src 'self'`).
    - **Rate Limiting:** Install `django-ratelimit`. Protect auth endpoints (`/accounts/login`, `/api/token`).
- **Tracking Infrastructure (The "Eyes"):**
    - Install `django-structlog` for JSON-formatted logs.
    - **Model:** `UserActivity` (fields: `user`, `event_type`, `metadata` JSONB, `session_id`, `ip_address`).
    - **Middleware:** `ActivityTrackingMiddleware` to associate anonymous sessions with authenticated users post-login.
    - **Granular Data Collection:**
        - **Context:** `connection_type` (4g/wifi), `device_type` (mobile/desktop).
        - **Behavior:** `dwell_time_ms` (time spent on specific Menu Item details), `scroll_depth` (did they see the footer?).
        - **Intent:** `search_term` (especially "zero result" searches), `active_filters` (e.g., user toggled "Vegan Only").

## Phase 1 – Web/PWA Polish (weeks 2–3: Feb 1–Feb 14, 2026)
**Goal:** A native-feeling web experience.

- **PWA Configuration:**
    - **Manifest:** `manifest.webmanifest` with `display: standalone`, `theme_color`, and maskable icons (Android 13+ support).
    - **Service Worker:** Implement `Workbox` via `django-serviceworker` or custom script.
        - *Strategy:* `StaleWhileRevalidate` for assets (CSS/JS/Fonts). `NetworkFirst` for HTML pages.
        - *Fallback:* Custom `offline.html` when network is unreachable.
- **UX & Performance:**
    - **Assets:** Convert hero images to WebP. Ensure all tap targets are ≥44px.
    - **Skeletons:** Add HTMX `htmx-indicator` CSS classes for loading states.
- **Client-Side Tracking (HTMX):**
    - Hook into `htmx:afterRequest` events.
    - Example: `hx-on::after-request="logEvent('view_item', {item_id: '123', dwell_start: Date.now()})"`
    - Track **"Cart Abandonment"**: Log when items are added vs. when checkout is completed.

## Phase 2 – API Surface (weeks 4–5: Feb 15–Feb 28, 2026)
**Goal:** REST API to support the mobile shell and future native clients.

- **Framework:** `djangorestframework` + `drf-spectacular` (for OpenAPI/Swagger docs).
- **Authentication:**
    - **JWT:** Use `djangorestframework-simplejwt`.
    - **Endpoints:** `/api/v1/auth/token/`, `/api/v1/auth/token/refresh/`.
    - **Custom Claims:** Add `role` and `avatar_url` to the token payload.
- **Core Resources:**
    - `/api/v1/menu/` (Read-only, cached).
    - `/api/v1/orders/` (Create, List history).
    - `/api/v1/cowork/spaces/` (Availability check).
- **CRM Integration:**
    - Use Django Signals (`post_save`) to update `UserStats` model.
    - *Trigger:* Order completed -> Increment `ltv`, update `last_seen`.
    - *Trigger:* Booking confirmed -> Tag user preference (e.g., "Private Room User").

## Phase 3 – Android APK & GitHub Distribution (weeks 6–7: Mar 1–Mar 14, 2026)
**Goal:** A "downloadable" app without the Play Store friction.

- **Capacitor Integration:**
    - `npm install @capacitor/core @capacitor/cli @capacitor/android`.
    - `npx cap add android`.
    - **Config:** Set `server.url` to production URL (allows live updates/OTA-like behavior for web assets).
- **Android Specifics:**
    - **Deep Links:** Configure `.well-known/assetlinks.json` on server and `<intent-filter>` in `AndroidManifest.xml`.
    - **Icons:** Generate adaptive icons using Android Studio Asset Studio.
- **Distribution:**
    - Build signed APK via GitHub Actions.
    - Upload artifacts to **GitHub Releases**.
    - Create a landing page: `36webapp.com/download` with a "How to Install" guide.

## Phase 4 – CRM & Analytics Dashboard (weeks 8–10: Mar 15–Mar 31, 2026)
**Goal:** Turn data into retention.

- **RFM Engine (Recency, Frequency, Monetary):**
    - Create a management command `calculate_rfm` to run nightly.
    - Score users 1-5 on each metric.
    - **Segments:** "Whales" (High M), "Loyalists" (High F), "At Risk" (Low R, High F).
- **Customer 360 View (The "Brain"):**
    - **Menu Affinity:** Tag users as "Vegan", "Decaf", "Sweet Tooth" based on order history (e.g., >3 orders of category X).
    - **Work Style:** Identify "Morning Larks" (books <9AM) vs. "Night Owls" (books >6PM).
    - **Price Sensitivity:** Analyze Average Order Value (AOV) and conversion rate on discounted items.
    - **Visuals:** Embed `Chart.js` in Admin to show personal spending trends and favorite seat heatmap.

## Phase 5 – The Unthinkable (Moonshots & Magic)
**Context:** Features that dissolve the barrier between physical and digital. High risk, extreme value.

1.  **Zero-UI "Ghost" Orders:**
    *   **Tech:** Bluetooth Low Energy (BLE) Beacons / WiFi BSSID triangulation.
    *   **Scenario:** User sits at **Table 4**. App detects Beacon `T4`.
    *   **Magic:** Notification pops up: *"Welcome back, Dante. The usual (Double Espresso)? Tap to confirm."*
    *   **Result:** Order placed and paid without opening the app menu.

2.  **"Open Sesame" Access:**
    *   **Tech:** NFC Host Card Emulation (HCE) or dynamic QR codes.
    *   **Scenario:** User books a desk.
    *   **Magic:** Phone acts as the keycard. Tapping the phone on the turnstile grants access. No reception check-in needed.

3.  **Serendipity Engine (Social Graph):**
    *   **Tech:** Graph DB + Vector Search (pgvector).
    *   **Scenario:** User checks in.
    *   **Magic:** *"A React developer just sat in the Quiet Zone. You're both working on Frontend. Want an intro?"* (Strict opt-in).

4.  **Barista Insight Engine (Smart Suggestions):**
    *   **Tech:** Sales velocity tracking + Historical comparison (Moving Averages).
    *   **Scenario:** A specialized "Barista HUD" dashboard on the cafe iPad.
    *   **Magic:** *"Good morning! It's raining today. Expect high demand for 'Hot Chocolate'. Top seller last Tuesday: 'Almond Croissant' - please verify stock levels."*

## Release Checklist (Per Deployment)
- [ ] `DEBUG=False`, `ALLOWED_HOSTS` set.
- [ ] DB Migrations applied.
- [ ] Static files collected & CDN cache purged.
- [ ] PWA Service Worker version bumped.
- [ ] Smoke test: Login, Book Seat, Order Coffee.