# Track Specification: Core Authentication System

## Objective
Implement a secure and localized authentication system for the 36 Webapp. This system must use phone numbers as the primary username and verify Iranian National IDs as the initial password. It must also support the Jalali calendar for any date-related fields (e.g., birthdate) and ensure full RTL support in all auth-related views.

## Core Features
1.  **Custom User Model:**
    -   `username` field: Iranian phone number (validated format, e.g., starting with 09...).
    -   `national_id` field: 10-digit Iranian National ID (validated using standard checksum algorithm).
    -   `birth_date`: Optional, using Jalali date.
2.  **Authentication Backends:**
    -   Allow login with Phone Number and Password (initially the National ID).
3.  **Registration Flow:**
    -   Form to collect: Phone Number, National ID, Full Name.
    -   Validate National ID integrity on submission.
    -   Create user with National ID as the hashed password.
4.  **Login Flow:**
    -   Standard login form expecting Phone Number and Password.
    -   RTL layout and Persian labels.
5.  **User Roles (Groups):**
    -   `Admin`: Full access.
    -   `Barista`: Access to cafe order management.
    -   `Customer`: Default role for new signups.
    -   Management command to initialize these groups.

## Technical Requirements
-   **Backend:** Django (Python).
-   **Database:** SQLite (Dev).
-   **Frontend:** Django Templates + TailwindCSS.
-   **Interactivity:** HTMX (for form validation/submission if needed, though standard POST is fine for auth).
-   **Localization:**
    -   All error messages in Persian.
    -   Templates must use `dir="rtl"`.
    -   Fonts should support Persian characters.

## Validation Rules
-   **Phone Number:** Must match Iranian mobile format regex (`^09\d{9}$`).
-   **National ID:**
    -   Must be 10 digits.
    -   Must satisfy the Iranian National ID checksum algorithm.
    -   Formula:
        -   Check digit is the 10th digit.
        -   Sum = (digit[0]*10 + digit[1]*9 + ... + digit[8]*2).
        -   Remainder = Sum % 11.
        -   If Remainder < 2, Check Digit should be Remainder.
        -   If Remainder >= 2, Check Digit should be 11 - Remainder.

## Design References
-   **Theme:** Dark mode primary.
-   **Style:** Minimalist, mobile-friendly forms.
