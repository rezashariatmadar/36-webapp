from django.test import TestCase, Client
from django.urls import reverse
from cowork.models import Space, PricingPlan
from accounts.factories import UserFactory

class CoworkUXTests(TestCase):
    def setUp(self):
        self.plan = PricingPlan.objects.create(name="Standard", hourly_rate=1000)
        self.space = Space.objects.create(
            name="Table 1", 
            zone=Space.ZoneType.LONG_TABLE, 
            pricing_plan=self.plan,
            is_active=True
        )
        self.client = Client()

    def test_space_list_hierarchical_structure(self):
        response = self.client.get(reverse('cowork:space_list'))
        self.assertEqual(response.status_code, 200)
        # Check for zone label
        self.assertContains(response, Space.ZoneType.LONG_TABLE.label)
        # Check for accordion structure
        self.assertContains(response, 'collapse-title')
        # Since we switched to client-side, the space name SHOULD be in the response
        self.assertContains(response, "Table 1")
        self.assertContains(response, 'card glass-panel glass-sheen hover-lift')
        self.assertNotContains(response, "floorplan.png")
        self.assertNotContains(response, "view = 'map'")

    def test_book_space_page_has_no_jquery_or_persian_datepicker_assets(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('cowork:book_space', args=[self.space.id]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "code.jquery.com")
        self.assertNotContains(response, "persian-datepicker")
        self.assertNotContains(response, "persian-date")
        self.assertContains(response, 'placeholder="YYYY-MM-DD"')
        self.assertNotContains(response, "hx-get=")
        self.assertNotContains(response, "hx-trigger=")
        self.assertNotContains(response, "unpkg.com/htmx.org@2.0.4")


class CoworkEmptyStateTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_space_list_empty_state_when_no_spaces_exist(self):
        response = self.client.get(reverse('cowork:space_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'در حال حاضر فضایی برای رزرو ثبت نشده')
