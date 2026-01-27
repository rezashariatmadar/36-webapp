from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    menu_view, add_to_cart, remove_from_cart, cart_detail, 
    checkout, order_list, barista_dashboard, update_order_status, 
    toggle_order_payment, admin_dashboard, manual_order_entry, 
    manage_menu_stock, MenuItemViewSet, PublicMenuItemViewSet,
    customer_lookup, reorder_order
)

app_name = 'cafe'

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)
router.register(r'public/menu', PublicMenuItemViewSet, basename='public-menu')

urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/reorder/', reorder_order, name='reorder_order'),
    
    # Barista Views
    path('dashboard/', barista_dashboard, name='barista_dashboard'),
    path('manual-order/', manual_order_entry, name='manual_order'),
    path('manage-menu/', manage_menu_stock, name='manage_menu'),
    path('lookup/', customer_lookup, name='customer_lookup'),
    
    # Analytics
    path('analytics/', admin_dashboard, name='admin_dashboard'),
    
    # Logic
    path('order/<int:order_id>/status/<str:new_status>/', update_order_status, name='update_order_status'),
    path('order/<int:order_id>/toggle-payment/', toggle_order_payment, name='toggle_order_payment'),
    
    # API
    path('api/', include(router.urls)),
]
