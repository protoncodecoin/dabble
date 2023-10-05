from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

from rest_framework import generics
from rest_framework.decorators import permission_classes

from dj_rest_auth.registration.views import RegisterView

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

from anime_api import permissions

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
# @permission_classes([permissions.IsCommonUser])
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
        # user.follows.add(creator)
        Follow.objects.create(user_from=user_prof, creator_to=creator)
        return Response(
            {"message": f"Successfully Following"}, status=status.HTTP_201_CREATED
        )
    else:
        # user.follows.remove(creator)
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
