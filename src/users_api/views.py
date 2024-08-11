from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic.base import View
from django.db.models import F, Q, Count


from rest_framework.views import APIView

from anime_api.models import (
    Anime,
    Design,
    Photography,
    Series,
    Text,
    Video,
    WrittenStory,
)


from .models import (
    CreatorProfile,
    Follow,
    CustomUser,
)
from .serializers import (
    MyTokenObtainPairSerializer,
    RCreatorSerializerDetail,
)

from rest_framework.decorators import api_view, action
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RCreatorSerializer, RCustomUserSerializer, RFollowSerializer

import requests

User = get_user_model()


# Create your views here


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenObtainPairView2(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Retreive tokens from the response
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")

        # set tokens in HTTP only cookies
        response = JsonResponse({"message": "Login successful"})
        response.set_cookie(
            "dabble_access_token",
            access_token,
            httponly=True,
            samesite="None",
            secure=True,
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        )
        response.set_cookie(
            "dabble_refresh_token",
            refresh_token,
            httponly=True,
            samesite="None",
            secure=True,
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        )

        return response


@api_view(["POST", "PUT"])
# @permission_classes([custom_permissions.IsCommonUser])
def follow_and_unfollow(request, creator_id):
    """
    Action to follow and unfollow a user
    """
    user = request.user

    try:
        user_prof = CreatorProfile.objects.get(creator=user)
        creator = CreatorProfile.objects.get(id=creator_id)
    except CreatorProfile.DoesNotExist:
        return Response(
            {
                "status": "error",
                "detail": f"Creator with the id of {creator_id} does not exists",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if not user_prof.following.filter(pk=creator.id).exists():
        Follow.objects.create(user_from=user_prof, user_to=creator)
        return Response(
            {"status": "ok", "message": True},
            status=status.HTTP_201_CREATED,
        )
    else:
        try:
            follow_relationship = Follow.objects.filter(
                user_from=user_prof, user_to=creator
            ).first()
        except Follow.DoesNotExist:
            print("relationship does not exist")
            return Response(
                {"message": "You don't follow this creator"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if follow_relationship is None:
            return Response(
                {"message": "error"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow_relationship.delete()
        return Response(
            {"status": "ok", "message": False},
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
def check_follow_status(request, creator_id):
    """
    Check the status if the authenticated user is following the other user or not
    """
    user = request.user

    try:
        user_prof = CreatorProfile.objects.get(creator=user)
        creator = CreatorProfile.objects.get(id=creator_id)
    except CreatorProfile.DoesNotExist:
        return Response(
            {
                "status": "error",
                "detail": f"Creator with the id of {creator_id} does not exists",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if user_prof.following.filter(pk=creator.id).exists():
        return Response({"message": True}, status=200)
    else:

        return Response({"message": False}, status=200)


@api_view(["POST"])
def check_like_fav_status(request, content_type, object_id):
    """
    Check if the post displayed has been liked and added to favorite by the user the authenticated user
    """
    added_to_fav = False
    liked = False

    content_type_mapping = {
        "anime": Anime,
        "story": WrittenStory,
        "designcontent": Design,
        "textcontent": Text,
        "videocontent": Video,
        "photography": Photography,
    }

    user = request.user
    selected_ct = content_type_mapping.get(content_type)

    try:
        creator_prof = CreatorProfile.objects.get(creator=user)
    except (CustomUser.DoesNotExist, CreatorProfile.DoesNotExist, ValueError):
        return Response({"error": "invalid user data"})
    if selected_ct:
        selected_ct.objects.get(id=object_id)

        print(selected_ct)

        # has user liked the post
        liked = selected_ct.objects.get(id=object_id)
        liked = liked.likes.filter(creator=user).exists()

        # has user added the post to favorites
        added_to_fav = selected_ct.objects.get(id=object_id)
        added_to_fav = added_to_fav.favorited_by.filter(creator=user).exists()

        return Response({"liked": liked, "favorited": added_to_fav})
    return Response({"error": "invalid content type"})


class CreatorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    This Viewset provides list, retrieve and update action for the Creatorprofile.
    The CreatorProfile is only created when a user signs up and should not be created through the serializer.
    """

    queryset = CreatorProfile.objects.all()
    serializer_class = RCreatorSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # check if user is authenticated
        # check if user is owner of object: update, partial_update

        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        # filter_backends = [DjangoFilterBackend]

        if self.action == "update":
            permission_classes = [permissions.IsAuthenticated]

        if self.action == "partial_update":
            permission_classes = [permissions.IsAuthenticated]

        if self.action == "update":
            # This is done to prevent normal user from making full update including creator* field having FK to the
            # AUTH_USER_MODEL. This will be implemented later
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    @action(detail=False)
    def top_creators(self, request):
        """
        A list of top creators
        """
        one_month_ago = timezone.now() - timedelta(days=30)

        top_series = (
            Series.objects.annotate(
                written_stories_count=Count("writtenstory_related"),
                anime_count=Count("anime_related"),
                # anime_likes_count=Count("anime_related__likes"),
                recent_anime=Count(
                    "anime_related",
                    filter=Q(anime_related__release_date__lte=one_month_ago),
                ),
                recent_written_stories=Count(
                    "writtenstory_related",
                    filter=Q(writtenstory_related__release_date__lte=one_month_ago),
                ),
            )
            .annotate(
                total_contributions=F("written_stories_count") + F("anime_count"),
                recent_contributions=F("recent_written_stories") + F("recent_anime"),
            )
            .order_by(
                "-total_contributions",
                "-recent_contributions",
            )[:10]
        )

        top_series_creators = [obj.creator for obj in top_series]
        top_creators_id = [obj.creator.id for obj in top_series]
        filtered_list = []
        for i in range(len(top_creators_id)):
            if top_creators_id[i] not in filtered_list:
                filtered_list.append(top_creators_id[i])
            else:
                top_series_creators.pop(i)
        page = self.paginate_queryset(top_series_creators)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({"message": 0}, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = CreatorProfile.objects.only(
            "id",
            "creator",
            "company_name",
            "company_website",
            "biography",
            "creator_logo",
        )
        serializer = RCreatorSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(data=serializer.data)

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        serializer = RCreatorSerializerDetail(
            instance,
            context={"request": request},
        )
        return Response(data=serializer.data)

    def update(self, request):
        instance = self.get_object()

        if instance.creator.email != self.request.user.email:
            return Response(
                {"message": "Not allowed", "status": status.HTTP_401_UNAUTHORIZED},
            )
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):

        instance = self.get_object()
        req_user = self.request.user.email

        if instance.creator.email != req_user:
            return Response(
                {"message": "Not allowed", "status": status.HTTP_401_UNAUTHORIZED},
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomUserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    This ViewSet provides list and retrieve action for the CustomUser model. This view can not be used to create CustomUser.
    """

    queryset = CustomUser.objects.all()
    serializer_class = RCustomUserSerializer


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    This ViewSet only returns a list of users
    """

    queryset = CreatorProfile
    serializer_class = RFollowSerializer
