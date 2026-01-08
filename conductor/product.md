# Product Guide - 36 Webapp

## Initial Concept
This project integrates a coworking space reservation system with a café management system for a seamless customer and staff experience. It leverages Django for the backend and Django Templates for the frontend to maintain a straightforward, modular implementation.

## Target Users
- **Coworking Members (Freelancers, Remote Workers):** Users who need to book seats, rooms, or desks and order from the cafe.
- **Café Staff (Baristas):** Staff responsible for managing the menu, processing orders, and updating order status.
- **System Administrators / Managers:** Users with full access to manage spaces, users, menu items, and view business analytics.
- **Walk-in Café Customers (Non-members):** Visitors who want to browse the menu and potentially place orders at the counter.

## Core Goals
- **Seamless Booking Experience:** Provide an interactive floor plan (based on the provided SVG layout) for easy reservation of various spaces.
- **Efficient Café Management:** Manage inventory and a diverse menu (Espresso Bar, Hot/Cold Drinks, Breakfast, Daily Meals, etc.) and streamline order processing.
- **Secure Authentication:** Implement a robust login system using phone numbers as usernames and validated Iranian National IDs as passwords.
- **Data-Driven Insights:** Provide an analytics dashboard to track top-selling items, loyal customers, and space occupancy rates.

## MVP Features
- **User Authentication & Roles:**
    - Login via Phone Number and Iranian National ID.
    - Futuristic "Access Terminal" login interface.
    - Role-based access for Admin, Barista, and Customer.
- **Coworking Space Management:**
    - "Space Command" dashboard with glass-panel tiles and interactive filters.
    - Support for Daily, Hourly, and Monthly reservations.
    - Zone-based booking rules (e.g., communal tables for daily use only).
- **Café Management:**
    - Menu management supporting categories from the provided menu (e.g., Espresso Bar, Shakes, Burgers, Pasta).
    - Digital ordering system with order queue for Baristas.
    - Order status tracking (Pending, Preparing, Ready, Delivered).
- **Admin & Analytics Dashboard:**
    - Management of users, spaces, and menu items.
    - Sales reports (top sellers, revenue) and customer analytics.
    - Space utilization metrics.
