from django.test import TestCase
from django.urls import reverse
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

    def test_user_list_api_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('accounts:api_user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_user_list_api_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('accounts:api_user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_user_list_api_anonymous(self):
        url = reverse('accounts:api_user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
