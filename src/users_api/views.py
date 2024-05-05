from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic.base import View


from rest_framework.views import APIView


from .models import (
    CreatorProfile,
    Follow,
    CustomUser,
)
from .serializers import (
    MyTokenObtainPairSerializer,
    RCreatorSerializerDetail,
)

from rest_framework.decorators import api_view
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from django.conf import settings
from django.http import HttpResponseRedirect
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
            {"status": "ok", "message": "Successfully Following"},
            status=status.HTTP_201_CREATED,
        )
    else:
        try:
            follow_relationship = Follow.objects.filter(
                user_from=user_prof, user_to=creator
            ).first()
        except Follow.DoesNotExist:
            return Response(
                {"message": "You don't follow this creator"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow_relationship.delete()
        return Response(
            {"status": "ok", "message": "Not following successful"},
            status=status.HTTP_204_NO_CONTENT,
        )


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

        if self.action == "update":
            permission_classes = [permissions.IsAuthenticated]

        if self.action == "partial_update":
            permission_classes = [permissions.IsAuthenticated]

        if self.action == "update":
            # This is done to prevent normal user from making full update including creator* field having FK to the AUTH_USER_MODEL.
            # This will be implemented later
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

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
