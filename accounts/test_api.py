from django.test import TestCase
from rest_framework.test import APIClient
from .factories import UserFactory
from django.contrib.auth.models import Group

class UserListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.admin = UserFactory()
        self.admin.groups.add(self.admin_group)
        self.user = UserFactory()
        self.url = "/api/auth/staff/users/"

    def test_user_list_api_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn("role", response.data[0])

    def test_user_list_api_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_list_api_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_list_pagination_shape(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.url}?page=1&page_size=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["page"], 1)
        self.assertEqual(response.data["page_size"], 1)
        self.assertEqual(len(response.data["results"]), 1)
