from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


from rest_framework import generics
from rest_framework.decorators import permission_classes


from .models import UserProfile, CreatorProfile, Follow, CustomUser
from .serializers import (
    UserProfileSerializer,
    UsersSerializer,
    CreatorProfileSerializer,
    CustomRegisterSerializer,
    MyTokenObtainPairSerializer,
)

from rest_framework.decorators import api_view
from rest_framework import permissions, status
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .models import Favorite
from .utility import create_favorite

from anime_api import permissions
from anime_api import models

User = get_user_model()


# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreatorListAPIView(generics.ListAPIView):
    """view for listing all creators"""

    queryset = CreatorProfile.objects.all()
    serializer_class = CreatorProfileSerializer


class UsersListAPIView(generics.ListAPIView):
    "view for listing all users"
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class AllUserListAPI(generics.ListAPIView):
    permission_classes = [permissions.EndPointRestrict]
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer


@api_view(["GET", "POST", "PUT"])
@permission_classes([permissions.IsCommonUser])
def follow_and_unfollow(request, creator_id):
    user = request.user
    user_prof = UserProfile.objects.get(user=user)
    try:
        creator = CreatorProfile.objects.get(id=creator_id)
    except CreatorProfile.DoesNotExist:
        return Response(
            {"detail": f"Creator with the id of {creator_id} does not exists"}
        )

    if not user_prof.follows.filter(pk=creator.id).exists():
        Follow.objects.create(user_from=user_prof, creator_to=creator)
        return Response(
            {"message": f"Successfully Following"}, status=status.HTTP_201_CREATED
        )
    else:
        try:
            follow_relationship = Follow.objects.filter(
                user_from=user_prof, creator_to=creator
            ).first()
        except Follow.DoesNotExist:
            return Response(
                {"message": "You don't follow this creator"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow_relationship.delete()
        return Response(
            {"message": f"Unfollow was successful"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["POST"])
@permission_classes([permissions.IsCommonUser])
def add_remove_favorite(request, content_type, content_id):
    user = request.user
    user_prof = UserProfile.objects.get(user=user)

    if request.method == "POST":
        output = create_favorite(
            request_user=user_prof, content_id=content_id, target_model=models.Series
        )
        if output:
            return Response(
                {"message": "successfully added to favorite"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "successfully deleted to favorite"},
                status=status.HTTP_200_OK,
            )

    if content_type == "stories":
        output = create_favorite(
            request_user=user_prof, content_id=content_id, target_model=models.Story
        )
        if output:
            return Response(
                {"message": "Favorite was removed successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "successfully added to favorite"},
                status=status.HTTP_200_OK,
            )

    if content_type == "anime":
        output = create_favorite(
            request_user=user_prof, content_id=content_id, target_model=models.Anime
        )
        if output:
            return Response(
                {"message": "Favorite was removed successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "successfully added to favorite"},
                status=status.HTTP_200_OK,
            )

    return Response(
        {"message": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST
    )
