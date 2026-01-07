from django.test import TestCase, Client
from django.urls import reverse
from cowork.models import Space, PricingPlan

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
        # Should NOT contain the space name yet (lazy loaded)
        self.assertNotContains(response, "Table 1")

    def test_space_list_htmx_load(self):
        # Simulate HTMX request for the specific zone
        headers = {'HTTP_HX_REQUEST': 'true'}
        url = reverse('cowork:space_list') + f'?zone={Space.ZoneType.LONG_TABLE}'
        response = self.client.get(url, **headers)
        
        self.assertEqual(response.status_code, 200)
        # Should now contain the space name
        self.assertContains(response, "Table 1")
        # Should verify it's the partial template (no base html html/body tags)
        self.assertNotContains(response, '<html')
