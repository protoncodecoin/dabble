from django.shortcuts import render

from rest_framework import generics

from .models import Comment
from .serializers import CommentSerializer


# Create your views here.
class CommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
