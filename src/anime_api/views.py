from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework import filters


from .models import Series, Story, Anime, Season

from comment_system.models import Comment

from .serializers import (
    SeriesSerializer,
    SeriesDetailSerializer,
    StorySerializer,
    StoryCreateSerializer,
    StoryDetailSerializer,
    AnimeSerializer,
    AnimeDetailSerializer,
    AnimeCreateSerializer,
    SeasonSerializer,
    SeasonCreateSerializer,
)

from . import permissions


@api_view(["GET"])
def search_contents(request):
    if request.method == "GET":
        query = request.GET.get("query")
        if query == None:
            query = ""

        series_result = Series.objects.filter(Q(series_name__icontains=query))
        series_serializer = SeriesSerializer(
            series_result, many=True, context={"request": request}
        )

        anime_result = Anime.objects.filter(
            Q(episode_title__icontains=query)
            | (Q(episode_number__icontains=query))
            | (Q(description__icontains=query))
        )
        anime_serializer = AnimeSerializer(
            anime_result, many=True, context={"request": request}
        )

        story_result = Story.objects.filter(
            Q(episode_title__icontains=query)
            | (Q(episode_number__icontains=query))
            | (Q(description__icontains=query))
        )
        story_serializer = StorySerializer(
            story_result, many=True, context={"request": request}
        )

        query_result = {
            "series": series_serializer.data,
            "anime": anime_serializer.data,
            "story": story_serializer.data,
        }

        return Response(query_result)


@api_view(["POST", "PUT"])
@permission_classes([permissions.IsCommonUser, permissions.IsStaff])
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


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([permissions.IsCommonUser, permissions.IsStaff])
def comments(request, content_type, content_id):
    user = request.user
    if request.method == "POST":
        if content_type == "series":
            target_content_type = ContentType.objects.get_for_model(Series)
            Comment.objects.update_or_create(
                user=user,
                target_ct=target_content_type,
                target_id=content_id,
                comment=request.POST.get("comment"),
            )
            return Response(
                {"message": "successful"},
                status=status.HTTP_201_CREATED,
            )

        if content_type == "anime":
            target_content_type = ContentType.objects.get_for_model(Anime)

            Comment.objects.create(
                user=user,
                target_ct=target_content_type,
                target_id=content_id,
                comment=request.POST.get("comment"),
            )
            return Response(
                {"message": "Comment was successfuly added"},
                status=status.HTTP_201_CREATED,
            )

        if content_type == "story":
            target_content_type = ContentType.objects.get_for_model(Story)

            Comment.objects.create(
                user=user,
                target_ct=target_content_type,
                target_id=content_id,
                comment=request.POST.get("comment"),
            )
            return Response(
                {"message": "Comment was successfuly added"},
                status=status.HTTP_201_CREATED,
            )

    if request.method == "DELETE":
        if content_type == "series":
            target_content_type = ContentType.objects.get_for_model(Series)
            existing_commnet = Comment.objects.filter(
                user=user,
                target_ct=target_content_type,
                target_id=content_id,
                comment=request.POST.get("comment"),
            )
            if existing_commnet:
                existing_commnet.delete()
                return Response(
                    {"message": "Content deleted"}, status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if content_type == "story":
            target_content_type = ContentType.objects.get_for_model(Story)
            existing_comment = Comment.objects.filter(
                user=user,
                target_ct=target_content_type,
                target_id=content_id,
                comment=request.POST.get("comment"),
            )
            if existing_comment:
                existing_comment.delete()
                return Response(
                    {"message": "Content deleted"}, status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if content_type == "anime":
            target_content_type = ContentType.objects.get_for_model(Anime)
            existing_comment = Comment.objects.filter(
                user=user,
                target_ct=target_content_type,
                target_id=content_id,
                comment=request.POST.get("comment"),
            )
            if existing_comment:
                existing_comment.delete()
                return Response(
                    {"message": "Content deleted"}, status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {
            "message": "Hmm it seems an unplanned circumstance has finally occurred. Check the data you are providing."
        }
    )


class SeriesListAPI(generics.ListAPIView):
    """Return all Series in DD to the endpoint"""

    # permission_classes = [
    #     permissions.CreatorAllStaffAllButEditOrReadOnly,
    # ]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^series_name", "^synopsis", "creator__company_name"]

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


class SeriesCreateAPI(generics.CreateAPIView):
    """Return all Series in DD to the endpoint"""

    # permission_classes = [permissions.IsCreatorMember]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def get_queryset(self):
        return Series.objects.all()


class SeriesDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """views for handling single instance of series model"""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer


class StoryListAPI(generics.ListAPIView):
    """Handles Story data from the Story Model"""

    queryset = Story.objects.filter(publish=True)
    serializer_class = StorySerializer


class StoryCreateAPI(generics.ListCreateAPIView):
    """Handles Story data from the Story Model"""

    queryset = Story.objects.filter(publish=True)
    serializer_class = StoryCreateSerializer


class StoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Provide Retrieve, Update and Delete functionality for Story Model"""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = Story.objects.all()
    serializer_class = StoryDetailSerializer


class AnimeListAPI(generics.ListAPIView):
    """View to serialize data from Anime model."""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class AnimeCreateAPI(generics.CreateAPIView):
    """View to serialize data from Anime model."""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = Anime.objects.all()
    serializer_class = AnimeCreateSerializer


class AnimeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """View for handling single instance of the Anime Model"""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = Anime.objects.all()
    serializer_class = AnimeDetailSerializer


class SeasonListAPI(generics.ListAPIView):
    """View for listing all season instances"""

    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


class SeasonCreateAPI(generics.CreateAPIView):
    """View for creating new season object"""

    queryset = Season.objects.all()
    serializer_class = SeasonCreateSerializer


class SeasonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting instance of season model"""

    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
