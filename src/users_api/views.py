from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView


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

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .models import Favorite
from .serializers import FavoriteSerializer
from .utility import create_favorite

from anime_api import permissions
from anime_api import models

User = get_user_model()


# Create your views here.


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1"
    client_class = OAuth2Client


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order for google login to work. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"


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


@api_view(["GET"])
def search_creators(request):
    if request.method == "GET":
        query = request.GET.get("query")
        if query is None:
            query = ""

        creator_result = CreatorProfile.objects.filter(
            Q(company_name__icontains=query)
            | (Q(company_website__icontains=query))
            | (Q(company_description__icontains=query))
        )

        creator_serializer = CreatorProfileSerializer(creator_result, many=True)
        return Response(creator_serializer.data)


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
        Follow.objects.create(user_from=user_prof, creator_to=creator)
        return Response(
            {"message": "Successfully Following"}, status=status.HTTP_201_CREATED
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
            {"message": "Unfollow was successful"}, status=status.HTTP_204_NO_CONTENT
        )


# @api_view(["POST"])
# @permission_classes([permissions.IsCommonUser])
# def add_remove_favorite(request, content_type, content_id):
#     user = request.user
#     user_prof = UserProfile.objects.get(user=user)

#     if request.method == "POST":
#         output = create_favorite(
#             request_user=user_prof, content_id=content_id, target_model=models.Series
#         )
#         if output:
#             return Response(
#                 {"message": output.data},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"message": "successfully deleted to favorite"},
#                 status=status.HTTP_204_NO_CONTENT,
#             )

#     if content_type == "stories":
#         output = create_favorite(
#             request_user=user_prof, content_id=content_id, target_model=models.Story
#         )
#         if output:
#             return Response(
#                 {"message": output.data},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"message": "Favorite was successfully removed"},
#                 status=status.HTTP_204_NO_CONTENT,
#             )

#     if content_type == "anime":
#         output = create_favorite(
#             request_user=user_prof, content_id=content_id, target_model=models.Anime
#         )
#         if output:
#             return Response(
#                 {"message": output.data},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"message": "Favorite was removed successfully"},
#                 status=status.HTTP_204_NO_CONTENT,
#             )

#     return Response(
#         {"message": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST
#     )


@api_view(["POST"])
@permission_classes([permissions.IsCommonUser])
def add_remove_favorite(request, content_type, content_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    content_type_mapping = {
        "series": models.Series,
        "stories": models.Story,
        "anime": models.Anime,
    }

    target_model = content_type_mapping.get(content_type)

    if not target_model:
        return Response(
            {"message": "Invalid content_type"}, status=status.HTTP_400_BAD_REQUEST
        )

    output = create_favorite(
        request_user=user_profile, content_id=content_id, target_model=target_model
    )

    if output:
        return Response({"message": output.data}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Favorite was successfully removed"},
            status=status.HTTP_204_NO_CONTENT,
        )


class FavoriteAPIView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
