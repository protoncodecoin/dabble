from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django.utils.text import slugify


from .models import Series, Story, Anime

from .serializers import SeriesSerializer, StorySerializer, AnimeSerializer


# Create your views here.
class SeriesListAPI(generics.ListCreateAPIView):
    """Return all Series in DD to the endpoint"""

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class SeriesDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """views for handling single instance of series model"""

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class StoryAPI(generics.ListCreateAPIView):
    """Handles Story data from the Story Model"""

    queryset = Story.objects.filter(publish=True)
    serializer_class = StorySerializer


class StoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Provide Retrieve, Update and Delete functionality for Story Model"""

    queryset = Story.objects.all()
    serializer_class = StorySerializer


class AnimeAPI(generics.ListCreateAPIView):
    """View to serialize data from Anime model."""

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class AnimeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """View for handling single instance of the Anime Model"""

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
