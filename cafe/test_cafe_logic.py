from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from .factories import MenuItemFactory, MenuCategoryFactory
from .models import MenuItem, CafeOrder, OrderItem, MenuCategory
from accounts.factories import UserFactory

class CafeLogicTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        # MenuItemFactory creates a MenuCategory via SubFactory
        self.item = MenuItemFactory(price=10000)

    def _get_request_with_session(self, url):
        request = self.factory.get(url)
        
        # Add session support
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        # Add messaging support
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_add_to_cart(self):
        from .views import add_to_cart
        url = reverse('cafe:add_to_cart', args=[self.item.id])
        request = self._get_request_with_session(url)
        
        add_to_cart(request, self.item.id)
        
        self.assertEqual(request.session['cart'][str(self.item.id)], 1)

    def test_remove_from_cart(self):
        from .views import remove_from_cart
        url = reverse('cafe:remove_from_cart', args=[self.item.id])
        request = self._get_request_with_session(url)
        request.session['cart'] = {str(self.item.id): 2}
        
        remove_from_cart(request, self.item.id)
        self.assertEqual(request.session['cart'][str(self.item.id)], 1)
        
        remove_from_cart(request, self.item.id)
        self.assertNotIn(str(self.item.id), request.session['cart'])

    def test_order_status_transitions(self):
        order = CafeOrder.objects.create(user=self.user)
        self.assertEqual(order.status, CafeOrder.Status.PENDING)
        
        order.status = CafeOrder.Status.PREPARING
        order.save()
        self.assertEqual(order.status, CafeOrder.Status.PREPARING)

    def test_menu_category_ordering(self):
        # Clear categories created by factories in setUp
        MenuCategory.objects.all().delete()
        
        cat2 = MenuCategoryFactory(name="Cat 2", order=2)
        cat1 = MenuCategoryFactory(name="Cat 1", order=1)
        
        categories = MenuCategory.objects.all()
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
