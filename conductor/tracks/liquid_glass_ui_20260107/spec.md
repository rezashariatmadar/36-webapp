# Specification: Liquid Glass UI Overhaul

## 1. Overview
Implement the "Liquid Glass" visual design language across the application. This involves creating a global animated "Deep Nebula" background, transforming structural elements (Navbar, Footer) into floating glass panels, and updating key views (Home, Auth, Coworking) to utilize translucent glass cards and high-contrast typography.

## 2. Functional Requirements

### 2.1. Core Visual Engine ("Deep Nebula")
-   **Background:** Fixed container (`.liquid-background`) covering the viewport with a dark neutral base (`Neutral-900`).
-   **Animation:** Animated "blobs" with infinite float animation and `blur(80px)`.
    -   Blob 1: Company Blue (#100370)
    -   Blob 2: Company Red (#63021f)
    -   Blob 3: Accent Cyan (#00b5ff) (lower opacity)
-   **Utility Class:** `.glass-panel` providing:
    -   Backdrop blur (`16px`)
    -   Transparent background (`rgba(255, 255, 255, 0.03)`)
    -   Subtle white border (`rgba(255, 255, 255, 0.08)`)

### 2.2. Structural Glass Layout
-   **Navbar:** Detach from top edge. Convert to floating glass panel (`m-4`, `rounded-2xl`, `sticky`). Remove solid branding colors.
-   **Footer:** Detach from bottom edge. Convert to matching floating glass panel.
-   **Dropdowns:** Apply glass panel styling to dropdown menus (Profile, Admin) instead of solid backgrounds.

### 2.3. Home Page ("The Landing")
-   **Hero Section:** Replace grey background with `.glass-panel`.
-   **Typography:** Main title ("۳۶") uses transparent background with gradient clip (`from-white to-accent`).
-   **Buttons:**
    -   Guest: Accent color for Login, Glass style for Register.
    -   User: "Logged in as" card uses nested transparency (`bg-white/5`).

### 2.4. Authentication Portals ("Access Terminals")
-   **Layout:** Center forms vertically and horizontally (`min-h-[80vh]`).
-   **Container:** Full glass card styling (`.glass-panel`, `shadow-2xl`).
-   **Inputs:** Transparent backgrounds (`bg-white/5`), white text, and subtle borders. Focus states with accent glow.
-   **Actions:** High-contrast Accent/Cyan submit buttons.

### 2.5. Coworking Dashboard ("Space Command")
-   **Filters:** Sticky glass control bar (`sticky top-24`, `z-40`) floating over content.
-   **Cards:** Space listings use glass panel styling. Hover effects (`hover:bg-white/5`).
-   **Status:** High-contrast text colors (Cyan for Available, Red/Ghost for Booked) with optional drop-shadows.
-   **Booking Page:** Split layout wrapped in a centralized glass panel.

## 3. Technical Constraints
-   **Stack:** Tailwind CSS, Django Templates.
-   **Scope:** `base.html`, `home.html`, `login.html`, `register.html`, `accounts/forms.py`, `cowork/space_list.html`, `cowork/book_space.html`.
-   **Performance:** Animations should use hardware-accelerated properties where possible.
