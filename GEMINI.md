# 36 Webapp - Context & Instructions

## Project Overview
**36 Webapp** is a unified platform for managing a coworking space and a café. It integrates seat/room reservations with a digital café ordering system. The application is built with a focus on **Persian (RTL) localization**, **Jalali calendar** support, and a seamless user experience for both customers and staff (Admins/Baristas).

## Technology Stack
- **Backend:** Python, Django 5.x
- **Frontend:** Django Templates, **Tailwind CSS**, **HTMX** (for interactivity/polling)
- **Database:** SQLite (Dev), PostgreSQL (Prod)
- **Localization:** `django-jalali` for dates, global `dir="rtl"`
- **Testing:** `pytest`, `factory-boy`

## Project Structure
| Directory | Purpose |
| :--- | :--- |
| `accounts/` | Custom user authentication (Phone + National ID), Role management (Admin, Barista, Customer). |
| `cafe/` | Menu management, Order processing, Inventory logic, Barista dashboard. |
| `cowork/` | Space/Seat definitions, Booking logic (Daily/Hourly/Monthly), Pricing plans, Interactive Floor Plan. |
| `theme/` | Frontend assets, Tailwind configuration (`static_src`), and base templates. |
| `conductor/` | Project documentation, product specs, and planning tracks. |
| `config/` | Main Django configuration (`settings.py`, `urls.py`). |

## Development Workflow

### 1. Backend Setup & Run
Standard Django commands apply.
```bash
# Activate virtual environment (if not active)
source .venv/bin/activate

# Apply migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 2. Frontend Development (Tailwind CSS)
The project uses `django-tailwind`. You likely need to run the Tailwind watcher in a separate terminal or background process to compile styles on the fly.
```bash
# Option A: Via Django command (if configured)
python manage.py tailwind start

# Option B: Direct NPM command
cd theme/static_src
npm install  # First time only
npm run dev
```

### 3. Testing
Tests are configured with `pytest`.
```bash
# Run all tests
pytest

# Run specific app tests
pytest cafe/
```

## Key Architectural Decisions & Conventions

### Authentication
- **Username:** Phone Number (validated format).
- **Password:** Iranian National ID (validated via checksum algorithm).
- **Roles:** Defined via Django Groups (`Admin`, `Barista`, `Customer`).

### Frontend Architecture
- **No SPA Frameworks:** Use standard Django templates.
- **Interactivity:** Use **HTMX** for dynamic content (e.g., polling for new orders, updating seat availability map).
    - `hx-trigger="every Xs"` for polling.
    - `hx-post` for actions.
- **Styling:** **Tailwind CSS** only. Do not write custom raw CSS unless necessary for complex animations or overrides.
- **RTL & Jalali:** Ensure all UI components support Right-to-Left layout and display dates in Jalali format.

### Domain Logic
- **Coworking:**
    - **Spaces:** Defined by `Zone` (e.g., Long Table, Private Room) which dictates booking rules (Daily-only vs Monthly).
    - **Availability:** Calculated dynamically based on `Booking` records.
    - **Floor Plan:** CSS Grid/Absolute positioning overlay on a static SVG/Image background.
- **Cafe:**
    - **Orders:** Linked to `User` (and optionally `Booking` for desk delivery).
    - **Workflow:** `Pending` -> `Preparing` -> `Ready` -> `Delivered`.

## Code Style & Standards
- **General:** Adhere to **Google Python Style Guide**.
- **Python:**
    - **Line Length:** Max 80 characters.
    - **Indentation:** 4 spaces (no tabs).
    - **Docstrings:** Required for all public modules, functions, classes, and methods (Google style).
    - **Type Hints:** Strongly encouraged for public APIs.
    - **Imports:** Grouped (Standard Lib, Third-Party, Local), one per line.
- **Naming:** `snake_case` for variables/functions, `PascalCase` for classes, `ALL_CAPS` for constants.

## Important Files
- `plan.md`: Current project status and roadmap.
- `conductor/product.md`: Detailed feature specifications.
- `theme/static_src/src/styles.css`: Main Tailwind input file.
- `config/settings.py`: Project settings (check here for installed apps and middleware).
