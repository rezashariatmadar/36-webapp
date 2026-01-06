from django.urls import path
from .views import (
    menu_view, add_to_cart, remove_from_cart, cart_detail, 
    checkout, order_list, barista_dashboard, update_order_status, 
    toggle_order_payment, admin_dashboard
)

app_name = 'cafe'

urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='order_list'),
    path('dashboard/', barista_dashboard, name='barista_dashboard'),
    path('analytics/', admin_dashboard, name='admin_dashboard'),
    path('order/<int:order_id>/status/<str:new_status>/', update_order_status, name='update_order_status'),
    path('order/<int:order_id>/toggle-payment/', toggle_order_payment, name='toggle_order_payment'),
]