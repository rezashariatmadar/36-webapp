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
        # Check for new button class 'btn-secondary'
        self.assertContains(response, 'btn-secondary')
        # Check for new size 'btn-sm'
        self.assertContains(response, 'btn-sm')

    def test_floating_cart_appears(self):
        # Initially no cart, so no FAB
        response = self.client.get(reverse('accounts:home'))
        self.assertNotContains(response, 'fixed bottom-6 left-6')
        
        # Add item to cart
        session = self.client.session
        session['cart'] = {str(self.item.id): 1}
        session.save()
        
        # Now FAB should appear
        response = self.client.get(reverse('accounts:home'))
        self.assertContains(response, 'fixed bottom-6 left-6')
        self.assertContains(response, 'badge-secondary')
