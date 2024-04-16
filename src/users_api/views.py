from django.contrib.auth import get_user_model
from django.shortcuts import redirect

# from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.views.generic.base import View

# from django.contrib.postgres.search import (
#     SearchVector,
#     SearchQuery,
#     SearchRank,
# )


from rest_framework import generics
from rest_framework.views import APIView

from anime_api.serializers import (
    AnimeFavoriteSerializer,
    SeriesFavoriteSerializer,
    StoryFavoriteSerializer,
)

from .models import UserProfile, CreatorProfile, Follow, CustomUser
from .serializers import (
    CreatorFollowersSerializer,
    UserProfileSerializer,
    UsersSerializer,
    CreatorProfileSerializer,
    MyTokenObtainPairSerializer,
)

from rest_framework.decorators import api_view
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


from anime_api import permissions as custom_permissions
from anime_api import models
from users_api.models import CreatorProfile

from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken

import requests

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


class CreatorDetailAPIView(generics.RetrieveUpdateAPIView):
    """View for showing details of creator."""

    queryset = CreatorProfile.objects.all()
    serializer_class = CreatorProfileSerializer

    def get(self, request, pk, format=None):
        try:
            creator_profile = CreatorProfile.objects.get(id=pk)
        except CreatorProfile.DoesNotExist:
            return Response(
                {"message": "Creator Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        creator_serializer = CreatorProfileSerializer(
            creator_profile, context={"request": request}
        )

        return Response({"result": creator_serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):

        if "creator_logo" in request.FILES:
            try:

                creator = CreatorProfile.objects.get(id=pk)

            except CreatorProfile.DoesNotExist:
                return Response(
                    {"message": "Creator Profile does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except UserProfile.DoesNotExist:
                return Response(
                    {"message": "User Profile does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if request.user == creator.creator.email:
                file = request.FILES["creator_logo"]
                extension = file.name.split(".")[-1]

                file.name = f"{creator.company_name}.{extension}"
                request.FILES["creator_logo"] = file

                return super().patch(request, *args, *kwargs)
            return Response(
                {"message": "REQUEST NOT PERMITTED"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CreatorFollowersAPIView(APIView):
    """
    list of creator followers
    """

    def get(self, request, creator_pk, format=None):
        """
        return followers based on creator
        """
        try:
            creator_profile = CreatorProfile.objects.get(creator=creator_pk)
        except CreatorProfile.DoesNotExist:
            return Response(
                {"message": "Creator Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        followers = creator_profile.followers.all()
        no_of_followers = followers.count()

        follower_serializer = CreatorFollowersSerializer(
            followers, many=True, context={"request": request}
        )
        return Response(
            {"result": follower_serializer.data, "total_followers": no_of_followers},
            status=status.HTTP_200_OK,
        )


class UsersProfileListAPIView(generics.ListAPIView):
    """view for listing all users Profile"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """Views for showing details of common user."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, pk, format=None):

        try:
            user_profile = UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        user_serializer = UserProfileSerializer(
            user_profile, context={"request": request}
        )
        return Response({"message": user_serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Handle partial update
        """
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        if request.user.email == user_profile.user.email:
            if user_profile:
                if "profile_img" in request.FILES:
                    file = request.FILES["profile_img"]
                    extension = file.name.split(".")[-1]

                    file.name = f"{user_profile.user.email}.{extension}"

                    request.FILES["profile_img"] = file
                    return super().patch(request, *args, *kwargs)

            return Response(
                {"message": "User Profile not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "NOT PERMITTED TO MAKE REQUEST"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class AllUsersListAPIView(generics.ListAPIView):
    """Listing all users"""

    permission_classes = [custom_permissions.EndPointRestrict]
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer


class FavoritedAPIView(APIView):
    """
    View to list all user favorites in the system.

    """

    def get(self, request, format=None):
        """
        Return a list of all user favorites.
        """
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        anime = models.Anime.objects.filter(favorited_by=user_profile)
        stories = models.Story.objects.filter(favorited_by=user_profile)
        series = models.Series.objects.filter(favorited_by=user_profile)

        anime_serializer = AnimeFavoriteSerializer(
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
                    {"anime": anime_serializer.data},
                    {"stories": stories_serializer.data},
                    {"series": series_serializer.data},
                ]
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST", "PUT"])
# @permission_classes([custom_permissions.IsCommonUser])
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


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


class GoogleAuthRedirect(View):
    permission_classes = [AllowAny]

    def get(self, request):

        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri=http://localhost:8000/callback/google"

        return redirect(redirect_url)


class GoogleRedirectURIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Extract the authorization code from the request URL
        code = request.GET.get("code")
        print(code, "===============")

        if code:
            # Prepare the requet paramter to exchange the authorization code for an access token
            token_endpoint = "https://oauth2.googleapis.com/token"
            token_params = {
                "code": code,
                "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                "redirect_uri": "http://localhost:8000/callback/google",
                "grant_type": "authorization_code",
            }

            # Make a POST request to exchange the authorization code for an access token
            response = requests.post(token_endpoint, data=token_params)

            if response.status_code == 200:
                access_token = response.json().get("access_token")

                if access_token:
                    # Make a request to fetch the user's profile information
                    profile_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo"
                    headers = {"Authorization": f"Bearer {access_token}"}
                    profile_response = requests.get(profile_endpoint, headers=headers)

                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        print(profile_data, "========= profile data ==========")
                        # Proceed with user creation or login
                        user_model = get_user_model()

                        # check if user exists
                        try:

                            user_exist = user_model.objects.get(
                                email=profile_data["email"]
                            )
                            refresh = RefreshToken.for_user(user_exist)
                            data["access"] = str(refresh.access_token)
                            data["refresh"] = str(refresh)

                            return Response(data, status=status.HTTP_201_CREATED)

                        except user_model.DoesNotExist:
                            profile_email = profile_data["email"]
                            new_user = user_model.objects.create(
                                email=profile_email,
                                username=profile_email.split("@")[0],
                                is_creator=True,
                            )
                            new_user.save()
                            new_creator = CreatorProfile.objects.create(
                                creator=new_user,
                                creator_logo=profile_data["picture"],
                            )
                            new_creator.save()
                            refresh = RefreshToken.for_user(new_user)
                            data["access"] = str(refresh.access_token)
                            data["refresh"] = str(refresh)

                            return Response(data, status=status.HTTP_201_CREATED)

            return Response({}, status=status.HTTP_400_BAD_REQUEST)
