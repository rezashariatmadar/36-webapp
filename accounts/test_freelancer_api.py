from django.test import TestCase
from rest_framework.test import APIClient

from .factories import UserFactory
from .models import FreelancerFlair, FreelancerProfile, FreelancerServiceOffering, FreelancerSpecialtyTag


class OwnerFreelancerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(phone_number="09125550000", full_name="Owner User")
        self.client.force_authenticate(user=self.user)
        self.specialty = FreelancerSpecialtyTag.objects.create(name="Frontend", slug="frontend")
        self.flair = FreelancerFlair.objects.create(name="Top Rated", slug="top-rated")

    def test_get_owner_profile_creates_draft(self):
        response = self.client.get("/api/auth/freelancer-profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["profile"]["status"], FreelancerProfile.Status.DRAFT)

    def test_patch_profile_updates_fields(self):
        self.client.get("/api/auth/freelancer-profile/")
        payload = {
            "headline": "Senior frontend engineer",
            "introduction": "Ready for remote projects",
            "work_types": ["remote", "project_based"],
            "specialty_ids": [self.specialty.id],
            "flair_ids": [self.flair.id],
            "custom_specialties": ["React", "TypeScript"],
        }
        response = self.client.patch("/api/auth/freelancer-profile/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["profile"]["headline"], payload["headline"])
        self.assertEqual(response.data["profile"]["specialty_ids"], [self.specialty.id])

    def test_submit_profile_sets_pending_status(self):
        self.client.get("/api/auth/freelancer-profile/")
        self.client.patch(
            "/api/auth/freelancer-profile/",
            {"headline": "Designer", "introduction": "Bio", "work_types": ["remote"]},
            format="json",
        )
        response = self.client.post("/api/auth/freelancer-profile/submit/", {}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["profile"]["status"], FreelancerProfile.Status.PENDING_APPROVAL)

    def test_service_crud_for_owner(self):
        self.client.get("/api/auth/freelancer-profile/")
        create_response = self.client.post(
            "/api/auth/freelancer-services/",
            {
                "title": "UI Audit",
                "description": "Detailed interface review",
                "delivery_mode": "remote",
                "starting_price": 1000000,
                "response_time_hours": 24,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        service_id = create_response.data["service"]["id"]

        patch_response = self.client.patch(
            f"/api/auth/freelancer-services/{service_id}/",
            {"title": "UI/UX Audit", "response_time_hours": 12},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data["service"]["title"], "UI/UX Audit")

        delete_response = self.client.delete(f"/api/auth/freelancer-services/{service_id}/")
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(FreelancerServiceOffering.objects.filter(id=service_id).exists())


class PublicFreelancerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.published_user = UserFactory(phone_number="09124440000", full_name="Published User")
        self.draft_user = UserFactory(phone_number="09124440001", full_name="Draft User")
        self.specialty = FreelancerSpecialtyTag.objects.create(name="SEO", slug="seo")

        self.published_profile = FreelancerProfile.objects.create(
            user=self.published_user,
            public_slug="published-user",
            headline="SEO Expert",
            introduction="I optimize websites.",
            status=FreelancerProfile.Status.PUBLISHED,
            is_public=True,
        )
        self.published_profile.specialties.add(self.specialty)

        FreelancerProfile.objects.create(
            user=self.draft_user,
            public_slug="draft-user",
            headline="Draft headline",
            introduction="Draft intro",
            status=FreelancerProfile.Status.DRAFT,
            is_public=True,
        )

    def test_public_list_returns_only_published_profiles(self):
        response = self.client.get("/api/freelancers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["public_slug"], "published-user")

    def test_public_detail_only_accessible_for_published_profiles(self):
        ok_response = self.client.get("/api/freelancers/published-user/")
        self.assertEqual(ok_response.status_code, 200)

        missing_response = self.client.get("/api/freelancers/draft-user/")
        self.assertEqual(missing_response.status_code, 404)

