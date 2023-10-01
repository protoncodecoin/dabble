from django.shortcuts import render

from rest_framework import generics

from .models import Follow
from .serializers import FollowSerializer, FollowDetailSerializer

# Create your views here.


class FollowAPIView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FollowDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowDetailSerializer
