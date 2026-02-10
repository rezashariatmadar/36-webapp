from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.factories import UserFactory


class StaffAnalyticsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = UserFactory()
        barista_group, _ = Group.objects.get_or_create(name="Barista")
        self.staff.groups.add(barista_group)
        self.user = UserFactory()

    def test_analytics_requires_staff(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/staff/analytics/overview/")
        self.assertEqual(response.status_code, 403)

    def test_analytics_for_staff(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get("/api/staff/analytics/overview/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("cafe_total", response.data)
        self.assertIn("top_items", response.data)

