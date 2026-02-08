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

    def test_cart_badge_appears(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertContains(response, 'id="cart-badge-desktop"')
        content = response.content.decode("utf-8")
        badge_tag = content.split('id="cart-badge-desktop"')[1].split(">")[0]
        self.assertIn("hidden", badge_tag)

        session = self.client.session
        session["cart"] = {str(self.item.id): 1}
        session.save()

        response = self.client.get(reverse("accounts:home"))
        content = response.content.decode("utf-8")
        badge_tag = content.split('id="cart-badge-desktop"')[1].split(">")[0]
        self.assertNotIn("hidden", badge_tag)


class CafeEmptyStateTests(TestCase):
    def test_menu_empty_state_route_redirects_to_spa(self):
        response = self.client.get(reverse("cafe:menu"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/cafe")
