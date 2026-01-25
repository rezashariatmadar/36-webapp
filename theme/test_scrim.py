from django.test import TestCase, Client
from django.urls import reverse

class ScrimWrapperTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_scrim_wrapper_present(self):
        """Verify that the scrim-wrapper class is applied to the body."""
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        # Check for the class presence
        self.assertContains(response, 'scrim-wrapper')
