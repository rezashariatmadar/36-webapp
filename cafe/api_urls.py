from django.urls import path

from .api_views import (
    CafeCartAPIView,
    CafeCartItemsAPIView,
    CafeCheckoutAPIView,
    CafeMenuAPIView,
    CafeOrdersAPIView,
    CafeReorderAPIView,
    CafeStaffCustomerLookupAPIView,
    CafeStaffMenuItemAvailabilityAPIView,
    CafeStaffMenuItemsAPIView,
    CafeStaffOrderPaymentToggleAPIView,
    CafeStaffOrdersAPIView,
    CafeStaffOrderStatusAPIView,
)

app_name = "cafe_api"

urlpatterns = [
    path("menu/", CafeMenuAPIView.as_view(), name="menu"),
    path("cart/", CafeCartAPIView.as_view(), name="cart"),
    path("cart/items/", CafeCartItemsAPIView.as_view(), name="cart_items"),
    path("checkout/", CafeCheckoutAPIView.as_view(), name="checkout"),
    path("orders/", CafeOrdersAPIView.as_view(), name="orders"),
    path("orders/<int:order_id>/reorder/", CafeReorderAPIView.as_view(), name="reorder"),
    path("staff/orders/", CafeStaffOrdersAPIView.as_view(), name="staff_orders"),
    path("staff/orders/<int:order_id>/status/", CafeStaffOrderStatusAPIView.as_view(), name="staff_order_status"),
    path("staff/orders/<int:order_id>/toggle-payment/", CafeStaffOrderPaymentToggleAPIView.as_view(), name="staff_order_toggle_payment"),
    path("staff/menu-items/", CafeStaffMenuItemsAPIView.as_view(), name="staff_menu_items"),
    path("staff/menu-items/<int:item_id>/toggle-availability/", CafeStaffMenuItemAvailabilityAPIView.as_view(), name="staff_menu_toggle"),
    path("staff/customer-lookup/", CafeStaffCustomerLookupAPIView.as_view(), name="staff_customer_lookup"),
]
