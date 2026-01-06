# Product Guidelines - 36 Webapp

## Tone and Voice
- **Professional and Corporate:** The system should feel reliable and business-oriented, instilling confidence in coworking members and management.

## Visual Identity & UI Design
- **Dark Theme Primary:** Leverage the existing dark-themed CSS to provide a sleek, modern, and high-tech aesthetic.
- **Persian-First & Strict RTL:** 
    - Full Right-to-Left (RTL) support is mandatory for all layouts.
    - Implement bidirectional text rendering to handle mixed-language content if necessary.
    - Ensure all text alignment, spacing, and component directionality adapt to Persian flow.
    - Use Farsi-appropriate typography and validate rendering with Persian characters.
- **Mobile-Responsive Triage:** Prioritize the mobile experience for café orders and quick seat checks, while maintaining a robust desktop view for admin tasks.
- **Material Design Principles:** Use clear hierarchy, elevations, and consistent interactions to guide users intuitively through the booking and ordering flows.

## Brand Messaging & Content Style
- **Jalali Calendar System:** All dates and time-based interactions must use the Jalali (Solar Hijri) calendar system. Localization should be thorough, including day and month names.
- **Concise and Action-Oriented:** Use direct, brief labels and instructions in Persian to ensure a fast and efficient user experience.
- **Staff-Focused Efficiency:** Design the Barista and Admin dashboards for high-speed operation, minimizing the number of clicks required for common actions.
- **Seat Status Visuals:**
    - **Red:** Reserved (must clearly display "Reserved until [Jalali Time]").
    - **Green:** Available for booking.
