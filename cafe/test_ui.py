from django.test import TestCase
from django.urls import reverse

from cafe.models import MenuCategory, MenuItem


class CafeUITests(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(name="Coffee")
        self.item = MenuItem.objects.create(
            name="Espresso",
            price=10000,
            category=self.category,
            is_available=True,
        )

    def test_menu_route_redirects_to_spa(self):
        response = self.client.get(reverse("cafe:menu"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/cafe")

    def test_legacy_home_redirects_to_spa(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app")


class CafeEmptyStateTests(TestCase):
    def test_menu_empty_state_route_redirects_to_spa(self):
        response = self.client.get(reverse("cafe:menu"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/cafe")
