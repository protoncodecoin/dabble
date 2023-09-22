from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

from django.contrib.auth import get_user_model

from rest_framework import generics

from dj_rest_auth.registration.views import RegisterView

from .models import UserProfile, CreatorProfile
from .serializers import (
    UserProfileSerializer,
    UsersSerializer,
    CreatorProfileSerializer,
    CustomRegisterSerializer,
)


User = get_user_model()


# Create your views here.


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


# class CustomRegisterView(RegisterView):
#     """Custom view to override the dj_rest_auth registration views"""

#     serializer_class = CustomRegisterSerializer


class CreatorList(generics.ListCreateAPIView):
    """view for listing all users"""

    queryset = CreatorProfile.objects.all()
    serializer_class = CreatorProfileSerializer
