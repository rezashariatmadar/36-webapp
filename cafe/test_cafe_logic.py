from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from cafe.cart_session import CART_SCHEMA_VERSION, get_cart, save_cart
from cafe.factories import MenuCategoryFactory, MenuItemFactory
from cafe.models import CafeOrder, MenuCategory, OrderItem
from accounts.factories import UserFactory


class CafeLogicTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.item = MenuItemFactory(price=10000)

    def _request_with_session(self, url="/", method="get", data=None):
        if method.lower() == "post":
            request = self.factory.post(url, data=data or {})
        else:
            request = self.factory.get(url, data=data or {})
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_get_cart_resets_malformed_payload(self):
        request = self._request_with_session("/api/cafe/cart/")
        request.session["cart"] = ["bad"]
        request.session["cart_v"] = 999

        cart = get_cart(request)

        self.assertEqual(cart, {})
        self.assertEqual(request.session["cart"], {})
        self.assertEqual(request.session["cart_v"], CART_SCHEMA_VERSION)

    def test_save_cart_persists_cart_and_version(self):
        request = self._request_with_session("/api/cafe/cart/")

        save_cart(request, {str(self.item.id): 2})

        self.assertEqual(request.session["cart"], {str(self.item.id): 2})
        self.assertEqual(request.session["cart_v"], CART_SCHEMA_VERSION)

    def test_order_status_transitions(self):
        order = CafeOrder.objects.create(user=self.user)
        self.assertEqual(order.status, CafeOrder.Status.PENDING)

        order.status = CafeOrder.Status.PREPARING
        order.save()
        self.assertEqual(order.status, CafeOrder.Status.PREPARING)

    def test_menu_category_ordering(self):
        MenuCategory.objects.all().delete()
        cat2 = MenuCategoryFactory(name="Cat 2", order=2)
        cat1 = MenuCategoryFactory(name="Cat 1", order=1)

        categories = list(MenuCategory.objects.all())
        self.assertEqual(categories[0], cat1)
        self.assertEqual(categories[1], cat2)

    def test_order_total_price_calculation(self):
        order = CafeOrder.objects.create(user=self.user)
        OrderItem.objects.create(order=order, menu_item=self.item, quantity=2, unit_price=10000)

        order.refresh_from_db()
        self.assertEqual(order.total_price, 20000)

        item2 = MenuItemFactory(price=5000)
        OrderItem.objects.create(order=order, menu_item=item2, quantity=1, unit_price=5000)

        order.refresh_from_db()
        self.assertEqual(order.total_price, 25000)
