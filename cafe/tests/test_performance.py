from django.test import TestCase
from rest_framework.test import APIClient

from cafe.factories import MenuItemFactory


class CartPerformanceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.items = MenuItemFactory.create_batch(10)
        session = self.client.session
        session["cart"] = {str(item.id): 1 for item in self.items}
        session["cart_v"] = 1
        session.save()

    def test_cart_endpoint_query_count(self):
        with self.assertNumQueries(2):
            response = self.client.get("/api/cafe/cart/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cart_count"], 10)

    def test_cart_endpoint_drops_missing_items(self):
        session = self.client.session
        session["cart"]["99999"] = 1
        session.save()

        response = self.client.get("/api/cafe/cart/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cart_count"], 10)
        self.assertNotIn("99999", self.client.session.get("cart", {}))
