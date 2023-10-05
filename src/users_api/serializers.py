from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

from django.contrib.auth.models import User
from django.db import transaction

from .models import UserProfile, CreatorProfile, CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["is_creator"] = user.is_creator
        token["email"] = user.email

        return token


class CustomRegisterSerializer(RegisterSerializer):
    """Customize the dj-rest-auth registerSerializer to include custom user models"""

    is_creator = serializers.BooleanField(default=False)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.is_creator = self.data.get("is_creator")
        user.email = self.data.get("email")
        user.save()

        is_creator = self.validated_data.get("is_creator")

        # Create a Profile based on the is_creator field
        if is_creator:
            creator_profile = CreatorProfile(creator=user)
            creator_profile.save()
        else:
            user_profile = UserProfile(user=user)
            user_profile.save()
        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "pk",
            "email",
            "is_creator",
        )
        read_only_fields = ("is_creator",)


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

    names_of_follows = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the User Profile"""

        model = UserProfile
        fields = [
            "pk",
            "follows",
            "profile_img",
            "names_of_follows",
        ]

    def get_names_of_follows(self, obj):
        all_follows = obj.follows.all()
        follower_names = list(map(lambda name: name.company_name, all_follows))
        return follower_names
