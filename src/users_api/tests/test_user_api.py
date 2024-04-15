"""
Test user api endpoints.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


from rest_framework.test import APIClient

from users_api.models import CreatorProfile


# CREATE_USER_URL = reverse("users:create")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_creator_profile(self):
        """Test creating creator profile is successful."""

        payload = {
            "email": "testuser2@example.com",
            "password": "testpassword123",
        }
        company_website = "http://www.testsite.com"
        company_name = "testsite"
        biography = "I'm a creator"

        user = create_user(**payload)
        creator_profile = CreatorProfile(
            creator=user,
            company_name=company_name,
            company_website=company_website,
            biography=biography,
        )

        self.assertEqual(user.email, payload["email"])  # type: ignore
        self.assertEqual(user.email, creator_profile.creator.email)  # type: ignore
        self.assertEqual(creator_profile.company_name, company_name)
        self.assertEqual(creator_profile.company_website, company_website)
        self.assertEqual(creator_profile.biography, biography)
