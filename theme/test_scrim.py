from django.test import TestCase, Client
from django.urls import reverse

class ScrimWrapperTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_scrim_wrapper_present(self):
        """Verify that the scrim-wrapper class is applied to the body."""
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="min-h-screen text-base-content flex flex-col scrim-wrapper"')
