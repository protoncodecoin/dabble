from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework.views import APIView

from .renderers import CustomJSONRenderer

from .models import (
    Series,
    WrittenStory,
    Anime,
    Season,
    Text,
    Design,
    Video,
)

from comment_system.models import Comment
from comment_system.serializers import CommentSerializer

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
    TextDetailSerializer,
    TextCreateSerializer,
    DesignSerializer,
    DesignDetailSerializer,
    VideoCreateSerializer,
    VideoDetailSerializer,
    AnimeFavoriteSerializer,
    StoryFavoriteSerializer,
    SeriesFavoriteSerializer,
)

from anime_api import models

from users_api.models import CreatorProfile, UserProfile
from users_api.serializers import (
    # CreatorProfileSerializer,
    RCreatorSerializer,
)


@api_view(["GET"])
def search(request, contenttype):
    """
    Search database by using contenttype(models) and the query provided.
    contenttype/models include: series, story, anime, creatorProfile.
    """
    content_type_mapping = {
        "series": models.Series,
        "anime": models.Anime,
        "story": models.WrittenStory,
        "creator": CreatorProfile,
    }

    target_content = content_type_mapping.get(contenttype)

    if target_content:
        if "query" in request.GET:
            query = request.GET.get("query")
            if query is None:
                query = ""

            if target_content == models.Anime:
                search_vector = SearchVector(
                    "episode_title", "description", "series__series_name"
                )
                search_query = SearchQuery(query)
                results = (
                    Anime.objects.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )
                anime_serializer = AnimeSerializer(
                    results, many=True, context={"request": request}
                )

                return Response(
                    {"result": anime_serializer.data}, status=status.HTTP_200_OK
                )

            if target_content == models.WrittenStory:
                search_vector = SearchVector(
                    "episode_title",
                    "description",
                    "series__series_name",
                    "content",
                )
                search_query = SearchQuery(query)
                results = (
                    WrittenStory.objects.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )
                story_serializer = StorySerializer(
                    results, many=True, context={"request": request}
                )

                return Response(
                    {"result": story_serializer.data}, status=status.HTTP_200_OK
                )

            if target_content == models.Series:
                search_vector = SearchVector(
                    "series_name",
                    "synopsis",
                )
                search_query = SearchQuery(query)
                results = (
                    Series.objects.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )
                series_serializer = SeriesSerializer(
                    results, many=True, context={"request": request}
                )

                return Response(series_serializer.data)

            if target_content == CreatorProfile:
                search_vector = SearchVector(
                    "company_name",
                    "company_website",
                    "biography",
                    "creator.creator",
                )
                search_query = SearchQuery(query)
                results = (
                    CreatorProfile.objects.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )
                creator_serializer = RCreatorSerializer(
                    results, many=True, context={"request": request}
                )

                return Response(
                    {"result": creator_serializer.data, status: status.HTTP_200_OK}
                )
        return Response({"message": "no query found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(
        {"message": "contenttype is incorrect."},
        status=status.HTTP_404_NOT_FOUND,
    )


@api_view(["POST", "PUT"])
# @permission_classes([permissions.IsCommonUser, permissions.IsStaff])
def toggle_like(request, content_id, content_type):
    """
    User actions: like && unlike
    User can like and unlike a Post
    """
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
                stories_instance = WrittenStory.objects.get(id=content_id)
            except WrittenStory.DoesNotExist:
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
                    status=status.HTTP_200_OK,
                )
        elif content_type == "animes":
            try:
                anime_instance = Anime.objects.get(id=content_id)
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

        elif content_type == "text":
            try:
                text_instance = Text.objects.get(pk=content_id)
                creator = CreatorProfile.objects.get(creator=user)
            except Text.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if not text_instance.likes.filter(creator=user).exists():
                text_instance.likes.add(creator)
                return Response(
                    {"message": "like was successful", "status": status.HTTP_200_OK}
                )
            else:
                text_instance.likes.remove(creator)
                return Response(
                    {"message": "like removed", "status": status.HTTP_204_NO_CONTENT}
                )

        elif content_type == "video":
            try:
                video_instance = Video.objects.get(pk=content_id)
                creator = CreatorProfile.objects.get(creator=user)
            except Video.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if not video_instance.likes.filter(creator=user).exists():
                video_instance.likes.add(creator)
                return Response(
                    {"message": "like was successful", "status": status.HTTP_200_OK}
                )
            else:
                video_instance.likes.remove(creator)
                return Response(
                    {"message": "like removed", "status": status.HTTP_204_NO_CONTENT}
                )

        elif content_type == "design":
            try:
                design_instance = Design.objects.get(pk=content_id)
                creator = CreatorProfile.objects.get(creator=user)
            except Design.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if not design_instance.likes.filter(creator=user).exists():
                design_instance.likes.add(creator)
                return Response(
                    {"message": "like was successful", "status": status.HTTP_200_OK}
                )
            else:
                design_instance.likes.remove(creator)
                return Response(
                    {"message": "like removed", "status": status.HTTP_204_NO_CONTENT}
                )
    return Response(
        {"detail": "content_id missing"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "POST", "PUT", "DELETE"])
# @permission_classes([permissions.IsCommonUser, permissions.IsStaff])
def comments(request, content_type, content_id):
    user = request.user
    if request.method == "GET":
        if content_type == "series":
            target_content_type = ContentType.objects.get_for_model(Series)
            result = Comment.objects.filter(
                content_type=target_content_type, object_id=content_id
            )
            comment_serializer = CommentSerializer(
                result, many=True, context={"request": request}
            )

            return Response(
                {"message": comment_serializer.data}, status=status.HTTP_200_OK
            )

        if content_type == "anime":
            target_content_type = ContentType.objects.get_for_model(Anime)
            result = Comment.objects.filter(
                content_type=target_content_type, object_id=content_id
            )
            comment_serializer = CommentSerializer(
                result, many=True, context={"request": request}
            )

            return Response(comment_serializer.data)

        if content_type == "story":
            target_content_type = ContentType.objects.get_for_model(WrittenStory)
            result = Comment.objects.filter(
                content_type=target_content_type, object_id=content_id
            )
            comment_serializer = CommentSerializer(
                result, many=True, context={"request": request}
            )

            return Response(comment_serializer.data)

    if request.method == "POST" or request.method == "PUT":
        user_profile = UserProfile.objects.get(user=user)
        if content_type == "series":
            target_content_type = ContentType.objects.get_for_model(Series)
            Comment.objects.update_or_create(
                user=user_profile,
                content_type=target_content_type,
                object_id=content_id,
                comment=request.POST.get("comment"),
            )
            return Response(
                {"message": "successful"},
                status=status.HTTP_201_CREATED,
            )

        if content_type == "anime":
            target_content_type = ContentType.objects.get_for_model(Anime)

            Comment.objects.create(
                user=user_profile,
                content_type=target_content_type,
                object_id=content_id,
                text=request.POST.get("comment"),
            )
            return Response(
                {"message": "Comment was successfuly added"},
                status=status.HTTP_201_CREATED,
            )

        if content_type == "story":
            target_content_type = ContentType.objects.get_for_model(WrittenStory)

            Comment.objects.create(
                user=user_profile,
                content_type=target_content_type,
                object_id=content_id,
                text=request.POST.get("comment"),
            )
            return Response(
                {"message": "Comment was successfuly added"},
                status=status.HTTP_201_CREATED,
            )

    if request.method == "DELETE":
        if content_type == "series":
            target_content_type = ContentType.objects.get_for_model(Series)
            existing_comment = Comment.objects.filter(
                user=user,
                content_type=target_content_type,
                object_id=content_id,
                text=request.POST.get("comment"),
            )
            if existing_comment:
                existing_comment.delete()
                return Response(
                    {"message": "Content deleted🚮"}, status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if content_type == "story":
            target_content_type = ContentType.objects.get_for_model(WrittenStory)
            existing_comment = Comment.objects.filter(
                user=user,
                content_type=target_content_type,
                object_id=content_id,
                text=request.POST.get("comment"),
            )
            if existing_comment:
                existing_comment.delete()
                return Response(
                    {"message": "Content deleted🚮"}, status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if content_type == "anime":
            target_content_type = ContentType.objects.get_for_model(Anime)
            existing_comment = Comment.objects.filter(
                user=user,
                content_type=target_content_type,
                object_id=content_id,
                text=request.POST.get("comment"),
            )
            if existing_comment:
                existing_comment.delete()
                return Response(
                    {"message": "Content deleted🚮"}, status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {"message": "Something went wrong.😢🤦‍♂️"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@api_view(["POST"])
def toggle_favorite(request, content_type, content_id):
    """Toggle User favorite."""
    if request.user.is_authenticated:
        user = request.user
        content_type_mapping = {
            "series": models.Series,
            "anime": models.Anime,
            "story": models.WrittenStory,
        }
        target_content = content_type_mapping.get(content_type)
        if target_content:
            if target_content == models.Anime:
                try:
                    anime_obj = Anime.objects.get(pk=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)
                except Anime.DoesNotExist or CreatorProfile.DoesNotExist:
                    return Response(
                        {
                            "message": "object does not exist",
                            "status": status.HTTP_404_NOT_FOUND,
                        }
                    )
                if anime_obj.favorited_by.filter(id=user_profile.id).exists():
                    anime_obj.favorited_by.remove(user_profile)
                    return Response(
                        {"message": "anime removed from favorites"},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                anime_obj.favorited_by.add(user_profile)
                return Response(
                    {"message": "anime added to favorites"}, status=status.HTTP_200_OK
                )

            if target_content == models.Series:

                try:
                    series_obj = Series.objects.get(pk=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)
                except CreatorProfile.DoesNotExist or Series.DoesNotExist:
                    return Response(
                        {
                            "message": "object does not exist",
                            "status": status.HTTP_404_NOT_FOUND,
                        }
                    )
                if series_obj.favorited_by.filter(id=user_profile.id).exists():
                    series_obj.favorited_by.remove(user_profile)
                    return Response(
                        {"message": "series removed from favorites"},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                series_obj.favorited_by.add(user_profile)
                return Response(
                    {"message": "series added to favorites"}, status=status.HTTP_200_OK
                )

            if target_content == models.WrittenStory:
                try:
                    story_obj = WrittenStory.objects.get(pk=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)
                except CreatorProfile.DoesNotExist or WrittenStory.DoesNotExist:
                    return Response(
                        {
                            "message": "object does not exist",
                            "status": status.HTTP_404_NOT_FOUND,
                        }
                    )
                if story_obj.favorited_by.filter(id=user_profile.id).exists():
                    story_obj.favorited_by.remove(user_profile)
                    return Response(
                        {"message": "story removed from favorites"},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                story_obj.favorited_by.add(user_profile)
                return Response(
                    {"message": "story added to favorites"}, status=status.HTTP_200_OK
                )

        return Response(
            {"message": "Invalid information provided to complete request"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        {"message": "Login to continue"}, status=status.HTTP_401_UNAUTHORIZED
    )


class FavoritedAPIView(APIView):
    """
    View to list all user favorites in the system.

    """

    def get(self, request, format=None):
        """
        Return a list of all user favorites.
        """
        user = request.user
        try:
            user_profile = CreatorProfile.objects.get(creator=user)
        except CreatorProfile.DoesNotExist:
            return Response(
                {"message": "User Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        anime = models.Anime.objects.filter(favorited_by=user_profile)
        stories = models.WrittenStory.objects.filter(favorited_by=user_profile)
        series = models.Series.objects.filter(favorited_by=user_profile)

        anime_serializer = AnimeFavoriteSerializer(
            anime, many=True, context={"request": request}
        )
        stories_serializer = StoryFavoriteSerializer(
            stories, many=True, context={"request": request}
        )
        series_serializer = SeriesFavoriteSerializer(
            series,
            many=True,
            context={"request": request},
        )
        return Response(
            {
                "message": [
                    {"anime": anime_serializer.data},
                    {"stories": stories_serializer.data},
                    {"series": series_serializer.data},
                ]
            },
            status=status.HTTP_200_OK,
        )


class SeriesListAPI(generics.ListAPIView):
    """Return all Series in DD to the endpoint"""

    # permission_classes = [
    #     permissions.CreatorAllStaffAllButEditOrReadOnly,
    # ]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    renderer_classes = [CustomJSONRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ["^series_name", "^synopsis", "creator__company_name"]

    def get_queryset(self):
        return Series.objects.all()


class SeriesCreateAPI(generics.CreateAPIView):
    """Return all Series in Database to the endpoint"""

    # permission_classes = [permissions.IsCreatorMember]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def get_queryset(self):
        return Series.objects.all()


class SeriesDetailAPI(generics.RetrieveUpdateAPIView):
    """views for handling single instance of series model"""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer


class StoryListAPI(generics.ListAPIView):
    """Handles Story data from the Story Model"""

    queryset = WrittenStory.objects.filter(publish=True)
    serializer_class = StorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^series__series_name", "^episode_title", "^description"]


class StoryCreateAPI(generics.ListCreateAPIView):
    """Handles Story data from the Story Model"""

    queryset = WrittenStory.objects.filter(publish=True)
    serializer_class = StoryCreateSerializer


class StoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Provide Retrieve, Update and Delete functionality for Story Model"""

    # permission_classes = [permissions.CreatorAllStaffAllButEditOrReadOnly]
    queryset = WrittenStory.objects.all()
    serializer_class = StoryDetailSerializer

    def delete(self, request, *args, **kwargs):

        if "pk" in kwargs:

            try:
                story_obj = WrittenStory.objects.get(pk=kwargs["pk"])
            except WrittenStory.DoesNotExist:
                return Response(
                    {"message": "Story not found", "status": status.HTTP_404_NOT_FOUND}
                )
            # if the user submitting the request isn't the same as the user that created the obj, reject the data and return an error
            if story_obj.series.creator.creator.email != request.user.email:
                return Response(
                    {"message": "Not permitted", "status": status.HTTP_401_UNAUTHORIZED}
                )
            # if the user is the same as the creator of the object
            return super().delete(request, *args, **kwargs)
        return Response(
            {"message": "Invalid pk provided", "status": status.HTTP_400_BAD_REQUEST}
        )


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

    def delete(self, request, *args, **kwargs):

        if "pk" in kwargs:

            try:
                anime_obj = Anime.objects.get(pk=kwargs["pk"])
            except Anime.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if anime_obj.series.creator.creator.email != request.user.email:
                return Response(
                    {"message": "Not permitted", "status": status.HTTP_401_UNAUTHORIZED}
                )
            return super().delete(request, *args, **kwargs)
        return Response(
            {"message": "Invalid pk provided", "status": status.HTTP_400_BAD_REQUEST}
        )


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

    def delete(self, request, *args, **kwargs):
        if "pk" in kwargs:
            try:
                season_obj = Season.objects.get(pk=kwargs["pk"])
            except Season.DoesNotExist:
                return Response(
                    {"message": "detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if season_obj:
                if request.user.email != season_obj.series.creator.creator.email:
                    return Response(
                        {
                            "message": "Not permitted",
                            "status": status.HTTP_401_UNAUTHORIZED,
                        }
                    )

                return self.destroy(request, *args, **kwargs)
            return Response(
                {
                    "message": "Invalid details provided",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )


class TextCreateAPIView(generics.ListCreateAPIView):
    """
    View to create text object.
    """

    queryset = Text.objects.all()
    serializer_class = TextCreateSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serailizer = TextCreateSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


class TextUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve single object
    update object
    delete object
    """

    queryset = Text.objects.all()
    serializer_class = TextDetailSerializer

    def delete(self, request, *args, **kwargs):
        text = self.get_object()
        req_user_prof = CreatorProfile.objects.get(creator=request.user)

        if text.creator != req_user_prof:
            return Response(
                {"detail": "You do not have the permission to delete this content"}
            )

        return self.destroy(request, *args, **kwargs)


class DesignCreateListAPIView(generics.ListCreateAPIView):
    """
    list and create design/illustration object
    """

    queryset = Design.objects.all()
    serializer_class = DesignSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serailizer = DesignSerializer(queryset, many=True, context={"request": request})
        return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


class DesignDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve: pk
    Update: pk
    Delete: pk
    """

    queryset = Design.objects.all()
    serializer_class = DesignDetailSerializer

    def delete(self, request, *args, **kwargs):
        design = self.get_object()
        req_user_prof = CreatorProfile.objects.get(creator=request.user)

        if design.creator != req_user_prof:
            return Response(
                {"detail": "You do not have the permission to delete this content"}
            )

        return self.destroy(request, *args, **kwargs)


class VideoCreateListAPIView(generics.ListCreateAPIView):
    """
    list and create design/illustration object
    """

    queryset = Video.objects.all()
    serializer_class = VideoCreateSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serailizer = VideoCreateSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


class VideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve: pk
    Update: pk
    Delete: pk
    """

    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer

    def delete(self, request, *args, **kwargs):
        video = self.get_object()
        req_user_prof = CreatorProfile.objects.get(creator=request.user)

        if video.creator != req_user_prof:
            return Response(
                {"detail": "You do not have the permission to delete this content"}
            )

        return self.destroy(request, *args, **kwargs)
