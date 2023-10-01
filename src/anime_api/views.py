from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


from .models import Series, Story, Anime

from .serializers import (
    SeriesSerializer,
    SeriesDetailSerializer,
    StorySerializer,
    StoryDetailSerializer,
    AnimeSerializer,
    AnimeDetailSerializer,
)
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


@api_view(["GET", "POST", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def like_and_unlike(request, content_id, content_type):
    user = request.user
    if content_id:
        if content_type == "series":
            try:
                series_instance = Series.objects.get(id=content_id)
            except Series.DoesNotExist:
                return Response(
                    {"message": f"Series with id of {content_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not series_instance.likes.filter(pk=user.id).exists():
                series_instance.likes.add(user)
                return Response(
                    {"message": "Like was successful"}, status=status.HTTP_200_OK
                )
            else:
                series_instance.likes.remove(user)
                return Response(
                    {"message": "UnLike was successful"},
                    status=status.HTTP_204_NO_CONTENT,
                )
        elif content_type == "stories":
            try:
                stories_instance = Series.objects.get(id=content_id)
            except Story.DoesNotExist:
                return Response(
                    {"message": f"Story with id of {content_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not stories_instance.likes.filter(pk=user.id).exists():
                stories_instance.likes.add(user)
                return Response(
                    {"message": "Like was successful"}, status=status.HTTP_200_OK
                )
            else:
                stories_instance.likes.remove(user)
                return Response(
                    {"message": "UnLike was successful"},
                    status=status.HTTP_204_NO_CONTENT,
                )
        elif content_type == "animes":
            try:
                anime_instance = Series.objects.get(id=content_id)
            except Anime.DoesNotExist:
                return Response(
                    {"message": f"Anime with id of {content_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not anime_instance.likes.filter(pk=user.id).exists():
                anime_instance.likes.add(user)
                return Response(
                    {"message": "Like was successful"}, status=status.HTTP_200_OK
                )
            else:
                anime_instance.likes.remove(user)
                return Response(
                    {"message": "UnLike was successful"},
                    status=status.HTTP_204_NO_CONTENT,
                )
    return Response(
        {"detail": "content_id missing"}, status=status.HTTP_400_BAD_REQUEST
    )


class SeriesListAPI(generics.ListCreateAPIView):
    """Return all Series in DD to the endpoint"""

    # queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    # lookup_field = "pk"

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_creator:
            return Response(
                {"detail": "Only creators can create a new series"},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            return serializer.save(creator=user)

    def get_queryset(self):
        return Series.objects.all()


class SeriesDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """views for handling single instance of series model"""

    permission_classes = (IsCreatorOrReaOnly,)
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer


class StoryAPI(generics.ListCreateAPIView):
    """Handles Story data from the Story Model"""

    queryset = Story.objects.filter(publish=True)
    serializer_class = StorySerializer


class StoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Provide Retrieve, Update and Delete functionality for Story Model"""

    # permission_classes = (IsCreatorOrReaOnly,)
    queryset = Story.objects.all()
    serializer_class = StoryDetailSerializer


class AnimeAPI(generics.ListCreateAPIView):
    """View to serialize data from Anime model."""

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class AnimeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """View for handling single instance of the Anime Model"""

    # permission_classes = (IsCreatorOrReaOnly,)
    queryset = Anime.objects.all()
    serializer_class = AnimeDetailSerializer
