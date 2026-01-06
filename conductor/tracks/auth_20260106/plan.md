# Track Plan: Core Authentication System

## Phase 1: Project & App Initialization
- [ ] Task: Initialize Django Project & Auth App
    -   Create a new Django app named `accounts` (or `users`).
    -   Configure `settings.py` for RTL, Timezone (Tehran), and add `accounts` to `INSTALLED_APPS`.
    -   Setup TailwindCSS integration (if not already done globally).

## Phase 2: Data Modeling & Validation
- [ ] Task: Implement National ID Validation Logic
    -   Create a utility function `validate_iranian_national_id(national_id)` in `accounts/utils.py`.
    -   Write unit tests for this validator (valid IDs, invalid checksums, wrong length).
- [ ] Task: Create Custom User Model
    -   Extend `AbstractBaseUser` and `PermissionsMixin`.
    -   Define `phone_number` as the `USERNAME_FIELD` (unique).
    -   Add `national_id` field.
    -   Add `full_name` and `birth_date` (optional).
    -   Create `CustomUserManager` to handle `create_user` and `create_superuser`.
    -   Make and run migrations.
- [ ] Task: Implement Phone Number Validation
    -   Add regex validator to the `phone_number` field on the model.

## Phase 3: Authentication Views & Forms
- [ ] Task: Create Registration Form
    -   Create a `UserRegistrationForm` (ModelForm).
    -   Override `clean()` to run the National ID validator.
    -   Ensure labels are in Persian.
- [ ] Task: Implement Registration View
    -   Create a view to handle registration.
    -   On success: Create user (set password = national_id), assign to 'Customer' group, and redirect to login.
- [ ] Task: Implement Login View
    -   Use or extend Django's `LoginView`.
    -   Create a custom `AuthenticationForm` if needed for Persian labels.
- [ ] Task: Create Templates (RTL)
    -   `registration/login.html`: Tailwind styled, dark theme, RTL.
    -   `registration/register.html`: Tailwind styled, dark theme, RTL.
    -   Ensure `dir="rtl"` is set on the `<html>` or container.

## Phase 4: Roles & Permissions
- [ ] Task: Initialize Groups
    -   Create a management command `init_roles` to create 'Admin', 'Barista', and 'Customer' groups.
    -   Run the command.

## Phase 5: Verification
- [ ] Task: Conductor - User Manual Verification 'Core Authentication System' (Protocol in workflow.md)