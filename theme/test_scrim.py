from django.test import TestCase, Client
from django.urls import reverse

class ScrimWrapperTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_spa_shell_body_classes_present(self):
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'min-h-screen bg-base-100 text-base-content')
