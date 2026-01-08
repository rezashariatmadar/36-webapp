from django.urls import reverse, resolve

def navigation(request):
    """
    Context processor to return primary navigation items based on user role.
    Items are defined as: {'label': str, 'url_name': str, 'roles': list, 'is_active': bool}
    """
    
    # Static navigation configuration
    # Roles: 'Admin', 'Barista', 'Customer', 'Anonymous' (or None for all)
    NAV_ITEMS = [
        # Customer / Public Items
        {
            'label': 'منو',
            'url_name': 'cafe:menu',
            'roles': ['Customer', 'Anonymous', 'Barista', 'Admin'],
        },
        {
            'label': 'رزرو فضا',
            'url_name': 'cowork:space_list',
            'roles': ['Customer', 'Anonymous', 'Barista', 'Admin'],
        },
        {
            'label': 'سفارش‌های من',
            'url_name': 'cafe:order_list',
            'roles': ['Customer'],
        },
        
        # Staff Items
        {
            'label': 'داشبورد',
            'url_name': 'cafe:barista_dashboard', # Default staff dash
            'roles': ['Barista', 'Admin'],
        },
        {
            'label': 'ثبت سفارش',
            'url_name': 'cafe:manual_order',
            'roles': ['Barista', 'Admin'],
        },
        {
            'label': 'مدیریت موجودی',
            'url_name': 'cafe:manage_menu',
            'roles': ['Barista', 'Admin'],
        },
    ]

    user = request.user
    user_roles = []
    
    if user.is_authenticated:
        if user.is_superuser or getattr(user, 'is_admin', False):
            user_roles.append('Admin')
        if getattr(user, 'is_barista', False):
            user_roles.append('Barista')
        # Assuming everyone authenticated is effectively a customer too, 
        # but we might want to segregate 'Customer' specific views if needed.
        # For this logic, we treat 'Customer' as "Authenticated non-staff" or general access.
        user_roles.append('Customer') 
    else:
        user_roles.append('Anonymous')

    visible_items = []
    current_url_name = None
    
    if request.resolver_match:
        current_url_name = request.resolver_match.view_name
        # Handle namespaced URLs (e.g., 'cafe:menu')
        if request.resolver_match.namespace:
            current_url_name = f"{request.resolver_match.namespace}:{request.resolver_match.url_name}"

    for item in NAV_ITEMS:
        # Check Role Access
        has_access = False
        for role in item['roles']:
            if role in user_roles:
                has_access = True
                break
        
        if has_access:
            # Clone dict to avoid mutating global config
            nav_item = item.copy()
            # Compute Active State
            # Simple exact match for now. Could verify namespace prefixes for "sections" later.
            nav_item['is_active'] = (current_url_name == nav_item['url_name'])
            
            try:
                nav_item['url'] = reverse(nav_item['url_name'])
                visible_items.append(nav_item)
            except:
                # Skip items if URL reversal fails (e.g. app not installed or misconfigured)
                continue

    return {'primary_nav': visible_items}
