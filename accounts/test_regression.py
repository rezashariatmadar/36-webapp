from django.test import TestCase
from django.urls import reverse

class CorePagesRegressionTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app')

    def test_login_page_loads(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_register_page_loads(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_cafe_menu_page_loads(self):
        response = self.client.get(reverse('cafe:menu'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cowork_space_list_page_loads(self):
        response = self.client.get(reverse('cowork:space_list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cowork')

    def test_profile_page_redirects_for_anonymous(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_user_list_page_redirects_for_anonymous(self):
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEqual(response.status_code, 302)
        # Should redirect to login because of admin_required (which usually uses login_required)
        self.assertIn('/app/account', response.url)

    def test_barista_dashboard_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:barista_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_my_bookings_page_redirects_for_anonymous(self):
        response = self.client.get(reverse('cowork:my_bookings'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cowork')

    def test_cafe_cart_detail_page_loads(self):
        response = self.client.get(reverse('cafe:cart_detail'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_checkout_page_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_order_list_page_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:order_list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_barista_dashboard_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:barista_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_customer_lookup_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:customer_lookup'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_manage_menu_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:manage_menu'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_manual_order_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:manual_order'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_admin_dashboard_redirects_for_anonymous(self):
        response = self.client.get(reverse('cafe:admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')
