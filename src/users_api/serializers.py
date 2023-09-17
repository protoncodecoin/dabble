from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

from django.contrib.auth.models import User
from django.db import transaction

from .models import UserProfile, CreatorProfile


class CustomRegisterSerializer(RegisterSerializer):
    is_creator = serializers.BooleanField(default=False)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.is_creator = self.data.get("is_creator")
        user.email = self.data.get("email")
        print(user.email)
        user.save()
        return user

    # implement signal to create profile based on registration type


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
            "is_creator",
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
