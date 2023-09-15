from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics

from .models import UserProfile, CreatorProfile
from .serializers import (
    UserProfileSerializer,
    UsersSerializer,
    CreatorProfileSerializer,
)

User = get_user_model()


# Create your views here.
class CreatorList(generics.ListCreateAPIView):
    """view for listing all users"""

    queryset = CreatorProfile.objects.filter(is_creator=True)
    serializer_class = CreatorProfileSerializer
