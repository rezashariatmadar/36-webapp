from django.test import TestCase
from django.urls import reverse
from cafe.models import MenuCategory, MenuItem

class CafeUITests(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(name='Coffee')
        self.item = MenuItem.objects.create(
            name='Espresso',
            price=10000,
            category=self.category,
            is_available=True
        )

    def test_menu_add_button_style(self):
        response = self.client.get(reverse('cafe:menu'))
        self.assertEqual(response.status_code, 200)
        # Check for new button class 'btn-primary'
        self.assertContains(response, 'btn-primary')
        # Check for new size 'btn-sm'
        self.assertContains(response, 'btn-sm')
        self.assertContains(response, 'data-rb-island="pixel-card"')

    def test_cart_badge_appears(self):
        # Initially badges are hidden (cart empty)
        response = self.client.get(reverse('accounts:home'))
        self.assertContains(response, 'id="cart-badge-desktop"')
        # Check that it has hidden class
        content = response.content.decode('utf-8')
        badge_tag = content.split('id="cart-badge-desktop"')[1].split('>')[0]
        self.assertIn('hidden', badge_tag)
        
        # Add item to cart
        session = self.client.session
        session['cart'] = {str(self.item.id): 1}
        session.save()
        
        # Now badges should NOT have 'hidden' class
        response = self.client.get(reverse('accounts:home'))
        content = response.content.decode('utf-8')
        badge_tag = content.split('id="cart-badge-desktop"')[1].split('>')[0]
        self.assertNotIn('hidden', badge_tag)


class CafeEmptyStateTests(TestCase):
    def test_menu_empty_state_is_visible_when_no_items_exist(self):
        response = self.client.get(reverse('cafe:menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'منو هنوز ثبت نشده است')
