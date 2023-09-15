from rest_framework import serializers

from django.contrib.auth.models import User

from .models import UserProfile, CreatorProfile


class UsersSerializer(serializers.ModelSerializer):
    """Serializer for Django User Model"""

    class Meta:
        """Meta class for the Django user Model"""

        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class CreatorProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Creator Profile"""

    class Meta:
        """Meta class for the Creator Profile"""

        model = CreatorProfile
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the User Profile"""

    class Meta:
        """Meta class for the User Profile"""

        model = UserProfile
        fields = "__all__"
