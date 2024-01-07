"""
Test for the animation API models.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from anime_api import models
from users_api import models as user_models

SERIES_URL = reverse("animes:series-create")


def detail_url(series_id):
    """Create and return the series object url"""
    return reverse("animes:series_create", args=[series_id])


class ModelTest(TestCase):
    """Test creation of object from Series models."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="creator@example.com", password="testpass123"
        )
        self.creator = user_models.CreatorProfile.objects.create(
            creator=self.user,
            company_name="star-anime",
            company_website="https://star-animations.com",
        )

    # def test_user_creation(self):
    #     """Test the creation of series object."""
    #     series_obj = models.Series.objects.create(
    #         creator=self.creator,
    #         series_name="attack on humans",
    #         synopsis="This is the synopsis",
    #     )

    #     print(SERIES_URL)

    #     # res = self.client.post(
    #     #     SERIES_URL, series_obj, headers={"Content-Type": "multipart/form-data"}
    #     # )

    #     # self.assertEqual(res.status_code, status.HTTP_201_CREATED)
