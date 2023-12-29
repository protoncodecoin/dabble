"""
Test model.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from users_api import models


class ModelTest(TestCase):
    """Test for user model."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123"
        )

    def test_common_user_creation(self):
        """Test commom user creation is successful without creator status."""

        email = "user1@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_creator)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com", "user2"],
            ["Testx3@Example.com", "Testx3@example.com", "user3"],
            # ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            # ["test4@example.com", "test4@example.com"],
        ]

        for email, expected, user in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password="sample123", username=user
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_super_user(self):
        """Test creating super user."""
        email = "superuser@admin.com"
        password = "supersecret"

        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)

    def test_creator_profile(self):
        """test creation of user profile."""
        creator_profile = models.CreatorProfile.objects.create(
            creator=self.user,
            company_name="star apple",
            company_website="https://star-apple.com/animations",
        )

        self.assertEqual(creator_profile.creator, self.user)
