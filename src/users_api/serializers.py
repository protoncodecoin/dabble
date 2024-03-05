from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

from django.contrib.auth.models import User
from django.db import transaction

from .models import UserProfile, CreatorProfile, CustomUser, Favorite

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from anime_api.models import Anime


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
        if user.is_creator:
            creator_group = Group.objects.get(name="creator")
            user.groups.add(creator_group)
        else:
            common_user_group = Group.objects.get(name="common_user")
            user.groups.add(common_user_group)
        user.save()

        is_creator = self.validated_data.get("is_creator")

        if is_creator:
            creator_profile = CreatorProfile(creator=user)
            creator_profile.save()
        else:
            user_profile = UserProfile(user=user)
            user_profile.save()
        return user


class UsersSerializer(serializers.ModelSerializer):
    """Serializer for Django User Model"""

    class Meta:
        """Meta class for the Django user Model"""

        model = CustomUser
        fields = [
            # "username",
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


class CreatorFollowersSerializer(serializers.ModelSerializer):
    """
    list of creator followers
    """

    user = serializers.ReadOnlyField(source="user.email")
    # number_of_follows = serializers.ReadOnlyField(source="")

    class Meta:
        model = UserProfile
        fields = [
            "user",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = "__all__"

    def get_user(self, obj):
        print(obj.content_type, "This is the obj")
        print(type(obj))
        print(obj.object_id)
        # fav_instance = Anime.objects.get(obj.object_id)
        return obj.user.user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the User Profile"""

    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        """Meta class for the User Profile"""

        model = UserProfile
        fields = [
            "pk",
            "user_email",
            "profile_img",
        ]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for the User Profile"""

    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        """Meta class for the User Profile"""

        model = UserProfile
        fields = [
            "pk",
            "user_email",
            "profile_img",
            "names_of_follows",
        ]
