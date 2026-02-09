def _is_active_path(request_path, prefixes):
    return any(request_path.startswith(prefix) for prefix in prefixes)


def navigation(request):
    """
    Context processor returning primary navigation items based on user roles.
    """
    nav_items = [
        {
            "label": "Menu",
            "url": "/app/cafe",
            "active_prefixes": ["/app/cafe"],
            "roles": ["Customer", "Anonymous", "Barista", "Admin"],
        },
        {
            "label": "Book Space",
            "url": "/app/cowork",
            "active_prefixes": ["/app/cowork"],
            "roles": ["Customer", "Anonymous", "Barista", "Admin"],
        },
        {
            "label": "My Orders",
            "url": "/app/cafe",
            "active_prefixes": ["/app/cafe"],
            "roles": ["Customer"],
        },
        {
            "label": "Staff Dashboard",
            "url": "/app/staff",
            "active_prefixes": ["/app/staff"],
            "roles": ["Barista", "Admin"],
        },
        {
            "label": "Manual Order",
            "url": "/app/staff",
            "active_prefixes": ["/app/staff"],
            "roles": ["Barista", "Admin"],
        },
        {
            "label": "Menu Stock",
            "url": "/app/staff",
            "active_prefixes": ["/app/staff"],
            "roles": ["Barista", "Admin"],
        },
    ]

    user = request.user
    user_roles = []
    if user.is_authenticated:
        if user.is_superuser or getattr(user, "is_admin", False):
            user_roles.append("Admin")
        if getattr(user, "is_barista", False):
            user_roles.append("Barista")
        user_roles.append("Customer")
    else:
        user_roles.append("Anonymous")

    request_path = request.path or ""
    visible_items = []
    for item in nav_items:
        has_access = any(role in user_roles for role in item["roles"])
        if not has_access:
            continue
        nav_item = item.copy()
        nav_item["is_active"] = _is_active_path(request_path, nav_item.get("active_prefixes", []))
        visible_items.append(nav_item)

    return {"primary_nav": visible_items}
