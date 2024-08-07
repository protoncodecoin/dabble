from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from users_api.models import CreatorProfile

from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# Create your views here.
class CommentAPIView(generics.ListCreateAPIView):
    # queryset = Comment.objects.filter(is_approved=True)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        req_user = self.request.user
        target_obj = self.request.data.get("target_id")
        content_type_str = self.request.data.get("target_ct")
        parent = self.request.data.get("parent", None)
        try:
            content_type = ContentType.objects.get(id=content_type_str)
            request_user = CreatorProfile.objects.get(creator=req_user)
        except ContentType.DoesNotExist:
            return Response(
                {"error": "Invalid content type"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(
            target_ct=content_type,
            target_id=target_obj,
            user=request_user,
            parent=parent,
        )

        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

        # serializer.save()


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
