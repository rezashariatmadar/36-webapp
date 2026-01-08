# Plan: Liquid Glass UI Overhaul

## Phase 1: The Foundation (Deep Nebula)
- [x] Task: Define CSS Animations & Classes in `base.html` 91e665e
    - [x] Sub-task: Create `.liquid-background` class (fixed, z-index -50, Neutral-900).
    - [x] Sub-task: Create `.blob` animation class and modifiers (Blue #100370, Red #63021f, Cyan #00b5ff).
    - [x] Sub-task: Create `.glass-panel` utility class (backdrop-blur, white/3 bg, white/8 border).
- [x] Task: Inject HTML Structure in `base.html` 91e665e
    - [x] Sub-task: Add `<div class="liquid-background">` with 3 blob children immediately inside `<body>`.
- [ ] Task: Conductor - User Manual Verification 'The Foundation (Deep Nebula)' (Protocol in workflow.md)

## Phase 2: Structural Glass (Floating Layout)
- [x] Task: Transform Navbar in `base.html` 5524fc3
    - [x] Sub-task: Remove solid backgrounds/borders. Add `.glass-panel`, floating margins (`m-4`), and rounded corners.
- [x] Task: Transform Footer in `base.html` 5524fc3
    - [x] Sub-task: Apply `.glass-panel` and floating margins to `<footer>`.
- [x] Task: Transform Dropdown Menus in `base.html` 5524fc3
    - [x] Sub-task: Apply `.glass-panel` to dropdown content containers.
- [ ] Task: Conductor - User Manual Verification 'Structural Glass (Floating Layout)' (Protocol in workflow.md)

## Phase 3: The Landing Experience
- [x] Task: Update Hero Section in `home.html` 5524fc3
    - [x] Sub-task: Replace solid background with `.glass-panel`.
- [x] Task: Update Typography in `home.html` 5524fc3
    - [x] Sub-task: Apply gradient text clip to main title ("۳۶").
- [x] Task: Update Buttons & Cards in `home.html` 5524fc3
    - [x] Sub-task: Style Login/Register buttons (Accent/Glass).
    - [x] Sub-task: Style User Info card with nested transparency.
- [ ] Task: Conductor - User Manual Verification 'The Landing Experience' (Protocol in workflow.md)

## Phase 4: Authentication Portals
- [x] Task: Update Form Styles in `accounts/forms.py` 5524fc3
    - [x] Sub-task: Update `CharField`, `EmailField`, `PasswordField` widgets with transparent Tailwind classes (`bg-white/5`, `text-white`, etc.).
- [x] Task: Update Login View in `registration/login.html` 5524fc3
    - [x] Sub-task: Center form layout. Wrap in `.glass-panel` card. Style submit button.
- [x] Task: Update Register View in `registration/register.html` 5524fc3
    - [x] Sub-task: Center form layout. Wrap in `.glass-panel` card. Style submit button.
- [ ] Task: Conductor - User Manual Verification 'Authentication Portals' (Protocol in workflow.md)

## Phase 5: Coworking & Dashboard Views
- [x] Task: Update Space List in `cowork/space_list.html` 5524fc3
    - [x] Sub-task: Style filter container as a sticky glass bar.
    - [x] Sub-task: Convert space cards to `.glass-panel` tiles with hover effects.
    - [x] Sub-task: Apply high-contrast colors to status indicators.
- [x] Task: Update Booking Page in `cowork/book_space.html` 5524fc3
    - [x] Sub-task: Wrap booking interface in a centralized glass panel.
- [ ] Task: Conductor - User Manual Verification 'Coworking & Dashboard Views' (Protocol in workflow.md)
