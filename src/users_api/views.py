from django.contrib.auth import get_user_model

# from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

# from django.contrib.postgres.search import (
#     SearchVector,
#     SearchQuery,
#     SearchRank,
# )


from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView

from anime_api.serializers import (
    AnimeDetailSerializer,
    AnimeFavoriteSerializer,
    SeriesFavoriteSerializer,
    StoryFavoriteSerializer,
)

from .models import UserProfile, CreatorProfile, Follow, CustomUser
from .serializers import (
    UserProfileSerializer,
    UsersSerializer,
    CreatorProfileSerializer,
    MyTokenObtainPairSerializer,
)

from rest_framework.decorators import api_view
from rest_framework import permissions, status
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
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


class CreatorDetailAPIView(generics.RetrieveAPIView):
    """View for showing details of creator."""

    queryset = CreatorProfile.objects.all()
    serializer_class = CreatorProfileSerializer


class UsersProfileListAPIView(generics.ListAPIView):
    """view for listing all users Profile"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    """Views for showing details of common user."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, pk, format=None):

        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_serializer = UserProfileSerializer(
            user_profile, context={"request": request}
        )
        return Response({"message": user_serializer.data}, status=status.HTTP_200_OK)


class AllUsersListAPIView(generics.ListAPIView):
    """Listing all users"""

    permission_classes = [permissions.EndPointRestrict]
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer


class FavoritedAPIView2(APIView):
    """
    View to list all user favorites in the system.

    """

    def get(self, request, format=None):
        """
        Return a list of all user favorites.
        """
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        anime = models.Anime.objects.filter(favorited_by=user_profile)
        stories = models.Story.objects.filter(favorited_by=user_profile)
        series = models.Series.objects.filter(favorited_by=user_profile)

        favorited_serializer = AnimeFavoriteSerializer(
            anime, many=True, context={"request": request}
        )
        stories_serializer = StoryFavoriteSerializer(
            stories, many=True, context={"request": request}
        )
        series_serializer = SeriesFavoriteSerializer(
            series,
            many=True,
            context={"request": request},
        )
        return Response(
            {
                "message": [
                    favorited_serializer.data,
                    stories_serializer.data,
                    series_serializer.data,
                ]
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST", "PUT"])
# @permission_classes([permissions.IsCommonUser])
def follow_and_unfollow(request, creator_id):
    user = request.user
    try:
        user_prof = UserProfile.objects.get(user=user)
        creator = CreatorProfile.objects.get(id=creator_id)
    except CreatorProfile.DoesNotExist:
        return Response(
            {
                "status": "error",
                "detail": f"Creator with the id of {creator_id} does not exists",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    except UserProfile.DoesNotExist:
        return Response(
            {"status": "error", "detail": "Sign up to perform this action."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user_prof.follows.filter(pk=creator.id).exists():
        Follow.objects.create(user_from=user_prof, creator_to=creator)
        return Response(
            {"status": "ok", "message": "Successfully Following"},
            status=status.HTTP_201_CREATED,
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
            {"status": "ok", "message": "Unfollow was successful"},
            status=status.HTTP_204_NO_CONTENT,
        )


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

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        print(len(queryset))
        for q in queryset.all():
            print(q)
        serializer = FavoriteSerializer(queryset, many=True)
        return Response(serializer.data)
