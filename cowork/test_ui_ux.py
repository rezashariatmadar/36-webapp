from django.test import Client, TestCase

from cowork.models import PricingPlan, Space


class CoworkUXTests(TestCase):
    def setUp(self):
        self.plan = PricingPlan.objects.create(name="Standard", hourly_rate=1000)
        self.space = Space.objects.create(
            name="Table 1",
            zone=Space.ZoneType.LONG_TABLE,
            pricing_plan=self.plan,
            is_active=True,
        )
        self.client = Client()

    def test_space_list_route_redirects_to_spa(self):
        response = self.client.get("/cowork/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/cowork")

    def test_book_space_route_redirects_to_spa(self):
        response = self.client.get(f"/cowork/book/{self.space.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/cowork")


class CoworkEmptyStateTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_space_list_empty_state_route_redirects_to_spa(self):
        response = self.client.get("/cowork/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/cowork")
