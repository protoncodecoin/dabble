from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.utils.text import slugify


from .models import Series, Story, Anime

from .serializers import SeriesSerializer, StorySerializer, AnimeSerializer
from .permissions import IsCreatorOrReaOnly


# Create your views here.
class GoogleLogin(SocialLoginView):
    adapter = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/v1/content/series/"
    client_class = OAuth2Client


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


class SeriesListAPI(generics.ListCreateAPIView):
    """Return all Series in DD to the endpoint"""

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class SeriesDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """views for handling single instance of series model"""

    permission_classes = (IsCreatorOrReaOnly,)
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class StoryAPI(generics.ListCreateAPIView):
    """Handles Story data from the Story Model"""

    queryset = Story.objects.filter(publish=True)
    serializer_class = StorySerializer


class StoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Provide Retrieve, Update and Delete functionality for Story Model"""

    permission_classes = (IsCreatorOrReaOnly,)
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class AnimeAPI(generics.ListCreateAPIView):
    """View to serialize data from Anime model."""

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class AnimeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """View for handling single instance of the Anime Model"""

    # permission_classes = (IsCreatorOrReaOnly,)
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
