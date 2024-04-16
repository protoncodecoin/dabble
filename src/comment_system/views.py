from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# Create your views here.
class CommentAPIView(generics.ListCreateAPIView):
    # queryset = Comment.objects.filter(is_approved=True)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        request_user = self.request.user
        target_obj = self.request.data.get("target_id")
        content_type_str = self.request.data.get("target_ct")

        try:
            content_type = ContentType.objects.get(id=content_type_str)
        except ContentType.DoesNotExist:
            return Response(
                {"error": "Invalid content type"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(target_ct=content_type, target_id=target_obj, user=request_user)

        return Response(
            {"message": "Comment Created Successfully"}, status=status.HTTP_201_CREATED
        )

        # serializer.save()


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
