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
        self.staff_user = UserFactory(is_staff=True)
        # MenuItemFactory creates a MenuCategory via SubFactory
        self.item = MenuItemFactory(price=10000)

    def _get_request_with_session(self, url, method="get", htmx=False, data=None):
        request_kwargs = {"HTTP_HX_REQUEST": "true"} if htmx else {}
        if method.lower() == "post":
            request = self.factory.post(url, data=data or {}, **request_kwargs)
        else:
            request = self.factory.get(url, data=data or {}, **request_kwargs)
        
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

    def test_add_to_cart_nonlegacy_htmx_redirects(self):
        from .views import add_to_cart

        url = f"/cafe/cart/add/{self.item.id}/"
        request = self._get_request_with_session(url, method="post", htmx=True)
        request.user = self.user

        response = add_to_cart(request, self.item.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cafe:menu"))

    def test_add_to_cart_legacy_hx_header_redirects(self):
        from .views import add_to_cart

        url = f"/legacy/cafe/cart/add/{self.item.id}/"
        request = self._get_request_with_session(url, method="post", htmx=True)
        request.user = self.user

        response = add_to_cart(request, self.item.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cafe:menu"))

    def test_update_order_status_nonlegacy_htmx_redirects(self):
        from .views import update_order_status

        order = CafeOrder.objects.create(user=self.user)
        request = self._get_request_with_session(
            f"/cafe/order/{order.id}/status/{CafeOrder.Status.PREPARING}/",
            method="post",
            htmx=True,
        )
        request.user = self.staff_user

        response = update_order_status(request, order.id, CafeOrder.Status.PREPARING)
        order.refresh_from_db()

        self.assertEqual(order.status, CafeOrder.Status.PREPARING)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cafe:barista_dashboard"))

    def test_update_order_status_legacy_hx_header_redirects(self):
        from .views import update_order_status

        order = CafeOrder.objects.create(user=self.user)
        request = self._get_request_with_session(
            f"/legacy/cafe/order/{order.id}/status/{CafeOrder.Status.PREPARING}/",
            method="post",
            htmx=True,
        )
        request.user = self.staff_user

        response = update_order_status(request, order.id, CafeOrder.Status.PREPARING)

        order.refresh_from_db()
        self.assertEqual(order.status, CafeOrder.Status.PREPARING)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cafe:barista_dashboard"))
