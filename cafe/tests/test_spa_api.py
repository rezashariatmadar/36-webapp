from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from accounts.factories import UserFactory
from cafe.factories import MenuCategoryFactory, MenuItemFactory
from cafe.models import CafeOrder, OrderItem
from cafe.views import MAX_CART_ITEMS


class CafeSPAApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.category = MenuCategoryFactory(name="Coffee")
        self.item = MenuItemFactory(category=self.category, is_available=True, price=120000)

    def test_menu_endpoint_returns_categories(self):
        response = self.client.get("/api/cafe/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["categories"]), 1)
        self.assertEqual(response.data["categories"][0]["name"], "Coffee")

    def test_cart_add_and_remove_item(self):
        add_response = self.client.post(
            "/api/cafe/cart/items/",
            {"menu_item_id": self.item.id, "delta": 1},
            format="json",
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.data["cart_count"], 1)

        remove_response = self.client.post(
            "/api/cafe/cart/items/",
            {"menu_item_id": self.item.id, "delta": -1},
            format="json",
        )
        self.assertEqual(remove_response.status_code, 200)
        self.assertEqual(remove_response.data["cart_count"], 0)

    def test_cart_item_delta_validation(self):
        response = self.client.post(
            "/api/cafe/cart/items/",
            {"menu_item_id": self.item.id, "delta": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_cart_rejects_unavailable_item(self):
        self.item.is_available = False
        self.item.save(update_fields=["is_available"])
        response = self.client.post(
            "/api/cafe/cart/items/",
            {"menu_item_id": self.item.id, "delta": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 409)

    def test_cart_limit_reached(self):
        session = self.client.session
        session["cart"] = {str(self.item.id): MAX_CART_ITEMS}
        session["cart_v"] = 1
        session.save()

        response = self.client.post(
            "/api/cafe/cart/items/",
            {"menu_item_id": self.item.id, "delta": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_checkout_requires_authentication(self):
        self.client.post("/api/cafe/cart/items/", {"menu_item_id": self.item.id, "delta": 1}, format="json")
        response = self.client.post("/api/cafe/checkout/", {"notes": "desk 3"}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_checkout_creates_order_and_clears_cart(self):
        self.client.post("/api/cafe/cart/items/", {"menu_item_id": self.item.id, "delta": 1}, format="json")
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/cafe/checkout/", {"notes": "desk 3"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CafeOrder.objects.filter(user=self.user).count(), 1)

        cart_response = self.client.get("/api/cafe/cart/")
        self.assertEqual(cart_response.status_code, 200)
        self.assertEqual(cart_response.data["cart_count"], 0)


class CafeStaffSPAApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = UserFactory()
        self.customer = UserFactory(phone_number="09125556666")

        barista_group, _ = Group.objects.get_or_create(name="Barista")
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        self.staff.groups.add(barista_group)
        self.customer.groups.add(customer_group)

        self.category = MenuCategoryFactory(name="Hot Drinks")
        self.item = MenuItemFactory(category=self.category, is_available=True, price=100000)

        self.order = CafeOrder.objects.create(user=self.customer, notes="desk 8", status=CafeOrder.Status.PENDING)
        OrderItem.objects.create(order=self.order, menu_item=self.item, quantity=2, unit_price=self.item.price)
        self.order.update_total_price()

    def test_staff_orders_requires_staff_role(self):
        regular_user = UserFactory()
        self.client.force_authenticate(user=regular_user)
        response = self.client.get("/api/cafe/staff/orders/")
        self.assertEqual(response.status_code, 403)

    def test_staff_orders_and_mutations(self):
        self.client.force_authenticate(user=self.staff)

        list_response = self.client.get("/api/cafe/staff/orders/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data["orders"]), 1)

        status_response = self.client.post(
            f"/api/cafe/staff/orders/{self.order.id}/status/",
            {"status": CafeOrder.Status.PREPARING},
            format="json",
        )
        self.assertEqual(status_response.status_code, 200)

        payment_response = self.client.post(f"/api/cafe/staff/orders/{self.order.id}/toggle-payment/", {}, format="json")
        self.assertEqual(payment_response.status_code, 200)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, CafeOrder.Status.PREPARING)
        self.assertTrue(self.order.is_paid)

    def test_staff_status_rejects_invalid_value(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            f"/api/cafe/staff/orders/{self.order.id}/status/",
            {"status": "NOT_A_REAL_STATUS"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_staff_menu_toggle_and_customer_lookup(self):
        self.client.force_authenticate(user=self.staff)

        menu_response = self.client.get("/api/cafe/staff/menu-items/")
        self.assertEqual(menu_response.status_code, 200)
        self.assertEqual(len(menu_response.data["items"]), 1)

        toggle_response = self.client.post(f"/api/cafe/staff/menu-items/{self.item.id}/toggle-availability/", {}, format="json")
        self.assertEqual(toggle_response.status_code, 200)
        self.item.refresh_from_db()
        self.assertFalse(self.item.is_available)

        lookup_response = self.client.get("/api/cafe/staff/customer-lookup/", {"q": "0912555"})
        self.assertEqual(lookup_response.status_code, 200)
        self.assertEqual(len(lookup_response.data["customers"]), 1)

    def test_staff_customer_lookup_by_name_and_empty_query(self):
        self.customer.full_name = "Customer SearchName"
        self.customer.save(update_fields=["full_name"])
        self.client.force_authenticate(user=self.staff)

        by_name = self.client.get("/api/cafe/staff/customer-lookup/", {"q": "SearchName"})
        self.assertEqual(by_name.status_code, 200)
        self.assertEqual(len(by_name.data["customers"]), 1)

        empty_query = self.client.get("/api/cafe/staff/customer-lookup/")
        self.assertEqual(empty_query.status_code, 200)
        self.assertEqual(empty_query.data["customers"], [])

    def test_staff_endpoints_require_staff_permission(self):
        regular_user = UserFactory()
        self.client.force_authenticate(user=regular_user)

        menu_response = self.client.get("/api/cafe/staff/menu-items/")
        self.assertEqual(menu_response.status_code, 403)

        toggle_response = self.client.post(
            f"/api/cafe/staff/menu-items/{self.item.id}/toggle-availability/",
            {},
            format="json",
        )
        self.assertEqual(toggle_response.status_code, 403)
