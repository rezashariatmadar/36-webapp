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
        # Check for new button class 'btn-accent'
        self.assertContains(response, 'btn-accent')
        # Check for new size 'btn-sm'
        self.assertContains(response, 'btn-sm')

    def test_floating_cart_appears(self):
        # Initially cart is hidden
        response = self.client.get(reverse('accounts:home'))
        self.assertContains(response, 'id="floating-cart"')
        self.assertContains(response, 'hidden')
        
        # Add item to cart
        session = self.client.session
        session['cart'] = {str(self.item.id): 1}
        session.save()
        
        # Now FAB should NOT have 'hidden' class
        response = self.client.get(reverse('accounts:home'))
        self.assertContains(response, 'id="floating-cart"')
        self.assertNotContains(response, 'id="floating-cart" class="fixed bottom-6 right-6 z-[150] animate-bounce hidden"')