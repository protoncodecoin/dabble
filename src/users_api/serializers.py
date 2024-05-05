from django.contrib.auth.models import Group

from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer

from django.db import transaction

from .models import UserProfile, CreatorProfile, CustomUser, Follow

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

    is_creator = serializers.BooleanField(default=True)

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


class RFollowSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer to serialize and deserialize data of Follow model
    """

    class Meta:
        model = Follow
        fields = [
            "url",
            "id",
            "user_from",
            "user_to",
        ]


class RCreatorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to serialize and deserialize data of the creatorProfile model
    """

    class Meta:
        model = CreatorProfile
        fields = [
            "id",
            "url",
            "creator",
            "company_name",
            "company_website",
            "biography",
            "creator_logo",
            # "following",
            # "followers",
        ]


class RCreatorSerializerDetail(serializers.HyperlinkedModelSerializer):
    """
    Serializer to serialize and deserialize data of the creatorProfile model
    """

    class Meta:
        model = CreatorProfile
        fields = [
            "id",
            "url",
            "creator",
            "company_name",
            "company_website",
            "biography",
            "creator_logo",
            "following",
            "followers",
        ]


class RCustomUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to serialize and deserialize data related to the CustomerUser model
    """

    user_profile = serializers.HyperlinkedIdentityField(
        view_name="creatorprofile-detail", read_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "user_profile",
        ]
