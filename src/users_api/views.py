from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

from rest_framework import generics

from dj_rest_auth.registration.views import RegisterView

from .models import UserProfile, CreatorProfile
from .serializers import (
    UserProfileSerializer,
    UsersSerializer,
    CreatorProfileSerializer,
    CustomRegisterSerializer,
)

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from dj_rest_auth.registration.views import SocialLoginView


User = get_user_model()


# Create your views here.


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/accounts/github/login/callback/"
    client_class = OAuth2Client


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/v1/content/stories/"
    # callback_url = "http://localhost:8000"
    client_class = OAuth2Client


# class CustomRegisterView(RegisterView):
#     """Custom view to override the dj_rest_auth registration views"""

#     serializer_class = CustomRegisterSerializer


class CreatorList(generics.ListCreateAPIView):
    """view for listing all users"""

    queryset = CreatorProfile.objects.all()
    serializer_class = CreatorProfileSerializer
