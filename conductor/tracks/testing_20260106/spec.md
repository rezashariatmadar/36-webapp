# Track Specification: Stability & Testing (v1.1)

## Overview
This track focuses on improving code quality and stability by implementing comprehensive unit tests for all existing modules (Accounts, Cafe, Cowork, API) and fixing persistent `NoReverseMatch` errors related to URL namespacing.

## Functional Requirements
- **URL Consistency**: Fix all `NoReverseMatch` errors by applying explicit namespacing (e.g., `accounts:logout`, `accounts:login`) across all templates, views, and redirects.
- **Accounts Testing**:
    - Validate National ID logic and Phone number regex.
    - Test User registration and Group assignment.
    - Verify RBAC decorators (`admin_required`, `barista_required`).
- **Cafe Testing**:
    - Verify Menu retrieval and category ordering.
    - Test Cart session logic (add/remove/total calculation).
    - Validate Order status transitions and Barista manual entry.
- **Coworking Testing**:
    - Test Space availability checks and conflict prevention.
    - Validate pricing calculations for all plans (Daily, Monthly, 6-Month, Yearly).
    - Enforce 8 AM - 8 PM operating hour constraints.
- **API Testing**:
    - Ensure REST endpoints return correct JSON structures and status codes.

## Non-Functional Requirements
- **Scalability**: Use `factory_boy` for generating consistent test data.
- **Coverage**: Aim for high code coverage on business logic and validation rules.
- **Standardization**: Adhere to Django's standard testing framework.

## Acceptance Criteria
- `python manage.py test` runs successfully for all apps (`accounts`, `cafe`, `cowork`).
- No `NoReverseMatch` errors occur during manual navigation or automated tests.
- All redirect URLs in views are verified to use namespaced names.

## Out of Scope
- Frontend styling or UI changes.
- Integration of deferred features (Zibal, Floor Plan Map).
