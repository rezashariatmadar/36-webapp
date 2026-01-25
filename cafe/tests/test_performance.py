from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from cafe.models import MenuItem
from cafe.factories import MenuItemFactory
from cafe.views import cart_detail
from django.db import connection, reset_queries
from django.contrib.auth.models import AnonymousUser

class CartPerformanceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.items = MenuItemFactory.create_batch(10)
        self.cart = {str(item.id): 1 for item in self.items}

    def _get_request_with_cart(self):
        url = reverse('cafe:cart_detail')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session['cart'] = self.cart
        request.session.save()
        request.htmx = False
        return request

    def test_cart_detail_query_count(self):
        request = self._get_request_with_cart()

        # Reset queries to ensure clean state
        reset_queries()

        with self.assertNumQueries(1):
            # Optimized: 1 query for all items
            cart_detail(request)

    def test_cart_missing_item_logging(self):
        # Add a non-existent item to cart
        self.cart['99999'] = 1
        request = self._get_request_with_cart()

        with self.assertLogs('cafe.views', level='WARNING') as cm:
            cart_detail(request)

        self.assertTrue(any("Item with ID 99999 found in cart" in output for output in cm.output))
