from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from anime_api.models import (
    Anime,
    Design,
    Photography,
    Series,
    Text,
    Video,
    WrittenStory,
)
from users_api.models import CreatorProfile

from .models import Comment
from .serializers import CommentListSerializer, CommentSerializer


# Create your views here.
class CommentAPIView(generics.CreateAPIView):
    # queryset = Comment.objects.filter(is_approved=True)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()

    def list(self, request):

        content_type_mapping = {
            # "series": Series,
            "anime": Anime,
            "textcontent": Text,
            "designcontent": Design,
            "videocontent": Video,
            "writtenstory": WrittenStory,
            "photography": Photography,
        }

        queryset = self.get_queryset()
        object_id = self.request.query_params.get("object_id")
        content_type = self.request.query_params.get("content_type")

        # check the content type and retrieve comment with the associated object id
        if object_id and content_type:
            target_model = content_type_mapping.get(content_type)

            # targe_model is a model from the content_type_mapping
            if target_model:
                post_data = target_model.objects.get(id=object_id)
                queryset = post_data.comments.all()

        serializer = CommentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
