from django.test import TestCase

class CorePagesRegressionTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')

    def test_login_page_loads(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_register_page_loads(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_cafe_menu_page_loads(self):
        response = self.client.get('/cafe/menu/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cowork_space_list_page_loads(self):
        response = self.client.get('/cowork/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cowork')

    def test_profile_page_redirects_for_anonymous(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_staff_user_api_denies_anonymous(self):
        response = self.client.get('/api/auth/staff/users/')
        self.assertEqual(response.status_code, 403)

    def test_barista_dashboard_redirects_for_anonymous(self):
        response = self.client.get('/cafe/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_my_bookings_page_redirects_for_anonymous(self):
        response = self.client.get('/cowork/my-bookings/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cowork')

    def test_cafe_cart_detail_page_loads(self):
        response = self.client.get('/cafe/cart/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_checkout_page_redirects_for_anonymous(self):
        response = self.client.get('/cafe/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_order_list_page_redirects_for_anonymous(self):
        response = self.client.get('/cafe/orders/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_barista_dashboard_redirects_for_anonymous(self):
        response = self.client.get('/cafe/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_customer_lookup_redirects_for_anonymous(self):
        response = self.client.get('/cafe/lookup/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_manage_menu_redirects_for_anonymous(self):
        response = self.client.get('/cafe/manage-menu/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_cafe_manual_order_redirects_for_anonymous(self):
        response = self.client.get('/cafe/manual-order/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_admin_dashboard_redirects_for_anonymous(self):
        response = self.client.get('/cafe/analytics/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')
