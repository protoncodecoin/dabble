from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils import timezone
from django.db.models import Count

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from anime_api.pagination import RecommendationPagination

from .models import (
    Photography,
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
    PhotographyCreateSerializer,
    PhotographyDetailSerializer,
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
    TextFavoriteSerializer,
    VideoFavoriteSerializer,
    DesignFavoriteSerializer,
)

from anime_api import models

from users_api.models import CreatorProfile, UserProfile
from users_api.serializers import (
    # CreatorProfileSerializer,
    RCreatorSerializer,
)

from library.models import Book
from library.pagination import CustomPagination
from library.serializers import BookSerializer


# connect to redis
# r = redis.Redis(
#     host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
# )


@api_view(["GET"])
def search(request, contenttype):

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
    try:
        user = CreatorProfile.objects.get(creator=request.user)
    except CreatorProfile.DoesNotExist:
        return Response(
            {"message": "User detail not found"}, status=status.HTTP_404_NOT_FOUND
        )
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
                    {"message": True, "content": "series"}, status=status.HTTP_200_OK
                )
            else:
                series_instance.likes.remove(user)
                return Response(
                    {"message": False, "content": "series"},
                    status=status.HTTP_200_OK,
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
                    {"message": True, "content": "stories"}, status=status.HTTP_200_OK
                )
            else:
                stories_instance.likes.remove(user)
                return Response(
                    {"message": False, "content": "stories"},
                    status=status.HTTP_200_OK,
                )
        elif content_type == "anime":
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
                    {"message": True, "content": "anime"}, status=status.HTTP_200_OK
                )
            else:
                anime_instance.likes.remove(user)
                return Response(
                    {"message": False, "content": "anime"},
                    status=status.HTTP_200_OK,
                )

        elif content_type == "text":
            try:
                text_instance = Text.objects.get(pk=content_id)

            except Text.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if not text_instance.likes.filter(pk=user.id).exists():
                text_instance.likes.add(user)
                return Response(
                    {"message": True, "status": status.HTTP_200_OK, "content": "text"}
                )
            else:
                text_instance.likes.remove(user)
                return Response(
                    {
                        "message": False,
                        "content": "text",
                        "status": status.HTTP_200_OK,
                    }
                )

        elif content_type == "video":
            try:
                video_instance = Video.objects.get(pk=content_id)

            except Video.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if not video_instance.likes.filter(pk=user.id).exists():
                video_instance.likes.add(user)
                return Response(
                    {"message": True, "content": "video", "status": status.HTTP_200_OK}
                )
            else:
                video_instance.likes.remove(user)
                return Response(
                    {
                        "message": False,
                        "content": "video",
                        "status": status.HTTP_200_OK,
                    }
                )

        elif content_type == "design":
            try:
                design_instance = Design.objects.get(pk=content_id)
            except Design.DoesNotExist:
                return Response(
                    {"message": "Detail not found", "status": status.HTTP_404_NOT_FOUND}
                )
            if not design_instance.likes.filter(pk=user.id).exists():
                design_instance.likes.add(user)
                return Response(
                    {
                        "message": True,
                        "content": "ddesign",
                        "status": status.HTTP_200_OK,
                    }
                )
            else:
                design_instance.likes.remove(user)
                return Response(
                    {
                        "message": False,
                        "content": "design",
                        "status": status.HTTP_200_OK,
                    }
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
                    {"message": "Content deleted🚮"}, status=status.HTTP_200_OK
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
            "book": Book,
            "text": Text,
            "design": Design,
            "video": Video,
            "photography": Photography,
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
                        {"message": False, "content": "anime"},
                        status=status.HTTP_200_OK,
                    )
                anime_obj.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "anime"}, status=status.HTTP_200_OK
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
                        {"message": False, "content": "series"},
                        status=status.HTTP_200_OK,
                    )
                series_obj.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "series"}, status=status.HTTP_200_OK
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
                        {"message": False, "content": "story"},
                        status=status.HTTP_200_OK,
                    )
                story_obj.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "story"}, status=status.HTTP_200_OK
                )

            if target_content == Book:
                try:
                    book_instance = Book.objects.get(id=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)

                except Book.DoesNotExist or CreatorProfile.DoesNotExist:
                    return Response(
                        {"message": "book not found"}, status=status.HTTP_404_NOT_FOUND
                    )
                if book_instance.favorited_by.filter(id=user.id).exists():
                    book_instance.favorited_by.remove(user_profile)
                    return Response(
                        {"message": False, "content": "book"},
                        status=status.HTTP_200_OK,
                    )
                book_instance.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "book"}, status=status.HTTP_200_OK
                )

            if target_content == Text:
                try:
                    text_instance = Text.objects.get(id=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)

                except (Text.DoesNotExist, CreatorProfile.DoesNotExist):
                    return Response(
                        {"message": "text content not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                if text_instance.favorited_by.filter(id=user.id).exists():
                    text_instance.favorited_by.remove(user_profile)
                    return Response(
                        {"message": False, "content": "text"},
                        status=status.HTTP_200_OK,
                    )
                text_instance.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "text"}, status=status.HTTP_200_OK
                )

            if target_content == Design:
                try:
                    design_instance = Design.objects.get(id=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)

                except (Design.DoesNotExist, CreatorProfile.DoesNotExist):
                    print("I do not exist=======")
                    return Response(
                        {"message": "design not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                if design_instance.favorited_by.filter(id=user.id).exists():
                    print("I was removed========")
                    design_instance.favorited_by.remove(user_profile)
                    return Response(
                        {"message": False, "content": "design"},
                        status=status.HTTP_200_OK,
                    )
                design_instance.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "design"}, status=status.HTTP_200_OK
                )

            if target_content == Video:
                try:
                    video_instance = Video.objects.get(id=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)

                except Video.DoesNotExist or CreatorProfile.DoesNotExist:
                    return Response(
                        {"message": "video content not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                if video_instance.favorited_by.filter(id=user.id).exists():
                    video_instance.favorited_by.remove(user_profile)
                    return Response(
                        {"message": False, "content": "video"},
                        status=status.HTTP_200_OK,
                    )
                video_instance.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "video"}, status=status.HTTP_200_OK
                )

            if target_content == Photography:
                try:
                    photography = Photography.objects.get(id=content_id)
                    user_profile = CreatorProfile.objects.get(creator=user)

                except Photography.DoesNotExist or CreatorProfile.DoesNotExist:
                    return Response(
                        {"message": "photography content not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                if photography.favorited_by.filter(id=user.id).exists():
                    photography.favorited_by.remove(user_profile)
                    return Response(
                        {"message": False, "content": "photography"},
                        status=status.HTTP_200_OK,
                    )
                photography.favorited_by.add(user_profile)
                return Response(
                    {"message": True, "content": "photography"},
                    status=status.HTTP_200_OK,
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

    def get(self, request, user_id, format=None):
        """
        Return a list of all user favorites.
        """
        user = user_id
        try:
            user_profile = CreatorProfile.objects.get(id=user)

        except CreatorProfile.DoesNotExist:
            return Response(
                {"message": "User Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        anime = models.Anime.objects.filter(favorited_by=user_profile)
        stories = models.WrittenStory.objects.filter(favorited_by=user_profile)
        series = models.Series.objects.filter(favorited_by=user_profile)
        text = models.Text.objects.filter(favorited_by=user_profile)
        video = models.Video.objects.filter(favorited_by=user_profile)
        design = models.Design.objects.filter(favorited_by=user_profile)
        books = Book.objects.filter(favorited_by=user_profile)

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
        text_serializer = TextFavoriteSerializer(text, many=True)
        video_serializer = VideoFavoriteSerializer(video, many=True)
        design_serializer = DesignFavoriteSerializer(design, many=True)
        books_serializer = BookSerializer(books, many=True)
        return Response(
            {
                "results": [
                    anime_serializer.data,
                    stories_serializer.data,
                    series_serializer.data,
                    text_serializer.data,
                    video_serializer.data,
                    design_serializer.data,
                    books_serializer.data,
                ]
            },
            status=status.HTTP_200_OK,
        )


class SeriesListAPI(generics.ListAPIView):
    """Return all Series in DB to the endpoint"""

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ["^series_name", "^synopsis", "creator__company_name"]

    def get_queryset(self):
        """
        This view returns a list of all series created by the user
        """
        queryset = Series.objects.all()
        user_id = self.request.query_params.get("id")
        user_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(creator=user_id)
            print(queryset.filter(creator=user_id))
        elif user_slug is not None:
            queryset = queryset.filter(creator__creator__username=user_slug)
        return queryset


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
    lookup_field = "pk"
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer


class StoryListAPI(generics.ListAPIView):
    """Handles Story data from the Story Model"""

    queryset = WrittenStory.objects.filter(publish=True)
    serializer_class = StorySerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ["^series__series_name", "^episode_title", "^description"]

    def get_queryset(self):
        queryset = WrittenStory.objects.all()

        user_id = self.request.query_params.get("id")
        story_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(series__creator=user_id)
        elif story_slug is not None:
            queryset = queryset.filter(slug=story_slug)

        return queryset


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

    def get_queryset(self):
        """
        Can be used to return objects filtered by either the user or the object's slug itself. It returns all items by default if no query_params is provided in the url
        """
        queryset = Anime.objects.all()

        user_id = self.request.query_params.get("id")
        anime_slug = self.request.query_params.get("slug")

        print("user id: ", user_id)

        if user_id is not None and not user_id == "":
            queryset = queryset.filter(series__creator=user_id)
        elif anime_slug is not None:
            queryset = queryset.filter(slug=anime_slug)
        return queryset

    def top_anime(self, request):
        """
        List of top 10 animations
        """
        one_month_ago = timezone.now() - timedelta(days=30)
        top_animation = (
            Anime.objects.filter(episode_release_date__gte=one_month_ago)
            .annotate(recent_likes_count=Count("likes"))
            .order_by("-recent_likes_count")[:10]
        )
        serializer = AnimeSerializer(top_animation, many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)


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

    def get_queryset(self):
        """
        Can be used to return objects filtered by either the user or the object's slug itself. It returns all items by default if no query_params is provided in the url
        """

        queryset = Season.objects.all()

        user_id = self.request.query_params.get("id")
        season_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(series__creator=user_id)
        elif season_slug is not None:
            queryset = queryset.filter(slug=season_slug)
        return queryset


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

    # queryset = Text.objects.all()
    serializer_class = TextCreateSerializer
    # renderer_classes = [CustomJSONRenderer]

    def get_queryset(self):
        """
        Can be used to return objects filtered by either the user or the object's slug itself. It returns all items by default if no query_params is provided in the url
        """

        queryset = Text.objects.all()

        user_id = self.request.query_params.get("id")
        text_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(creator=user_id)
        elif text_slug is not None:
            queryset = queryset.filter(slug=text_slug)
        return queryset

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serailizer = TextCreateSerializer(
    #         queryset, many=True, context={"request": request}
    #     )
    #     return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


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

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serailizer = DesignSerializer(queryset, many=True, context={"request": request})
    #     return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


class DesignDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve: pk
    Update: pk
    Delete: pk
    """

    # queryset = Design.objects.all()
    serializer_class = DesignDetailSerializer

    def get_queryset(self):
        """
        Can be used to return objects filtered by either the user or the object's slug itself. It returns all items by default if no query_params is provided in the url
        """

        queryset = Design.objects.all()

        user_id = self.request.query_params.get("id")
        design_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(creator=user_id)
        elif design_slug is not None:
            queryset = queryset.filter(slug=design_slug)
        return queryset

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

    # queryset = Video.objects.all()
    serializer_class = VideoCreateSerializer

    def get_queryset(self):
        """
        Can be used to return objects filtered by either the user or the object's slug itself. It returns all items by default if no query_params is provided in the url
        """

        queryset = Video.objects.all()

        user_id = self.request.query_params.get("id")
        video_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(creator=user_id)
        elif video_slug is not None:
            queryset = queryset.filter(slug=video_slug)
        return queryset

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serailizer = VideoCreateSerializer(
    #         queryset, many=True, context={"request": request}
    #     )
    #     return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


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


@api_view(["GET"])
def filter_by_similarity(request, content_type, content_id):
    """
    param:
        content_type: model
    Filter posts by similarity by using tags.
    """
    content_type_mapping = {
        "series": models.Series,
        "anime": models.Anime,
        "story": models.WrittenStory,
        # "creator": CreatorProfile,
        "text": models.Text,
        "video": models.Video,
        "design": models.Design,
    }
    target_content = content_type_mapping.get(content_type)

    if target_content == models.Anime:
        try:
            anime_obj = Anime.objects.get(id=content_id)
        except Anime.DoesNotExist:
            return Response({"results": []}, status=200)

        # Retrive ids of the anime obj
        anime_tag_ids = anime_obj.tags.values_list("id", flat=True)

        # Get all anime with same tags from the database
        similar_animation = Anime.objects.filter(tags__in=anime_tag_ids).exclude(
            id=anime_obj.id  # type: ignore
        )
        similar_animation = similar_animation.annotate(
            same_tags=Count("tags")
        ).order_by("same_tags")

        animation_serializer = AnimeSerializer(
            similar_animation, many=True, context={"request": request}
        )
        return Response({"resutls": animation_serializer.data}, status=200)

    elif target_content == models.WrittenStory:
        try:
            writtenstory_obj = WrittenStory.objects.get(id=content_id)
        except WrittenStory.DoesNotExist:
            return Response({"results": []}, status=200)

        # Retrieve ids of the written story obj
        written_story_ids = writtenstory_obj.tags.values_list("id", flat=True)

        # Get all written stories with same tags from the database
        similar_stories = WrittenStory.objects.filter(
            tags__in=written_story_ids
        ).exclude(id=writtenstory_obj.id)
        similar_stories = similar_stories.annotate(same_tags=Count("tags")).order_by(
            "same_tags"
        )
        # serialize the data
        written_stories_serializer = StorySerializer(
            similar_stories, many=True, context={"request": request}
        )
        return Response({"results": written_stories_serializer.data}, status=200)

    elif target_content == models.Text:
        try:
            text_obj = Text.objects.get(id=content_id)
        except Text.DoesNotExist:
            return Response({"results": []}, status=200)

        # Retrieve ids of the text obj
        text_tags_ids = text_obj.tags.values_list("id", flat=True)

        # Get all text from the database with same tags
        similar_texts = Text.objects.filter(tags__in=text_tags_ids).exclude(
            id=text_obj.id
        )
        similar_texts = similar_texts.annotate(similar_tags=Count("tags")).order_by(
            "similar_tags"
        )

        # serialize data
        similar_text_serializer = TextCreateSerializer(
            similar_texts, many=True, context={"request": request}
        )
        return Response({"results": similar_text_serializer.data}, status=200)

    elif target_content == models.Video:
        try:
            video_obj = Video.objects.get(id=content_id)
        except Video.DoesNotExist:
            return Response({"results": []}, status=200)

        video_tags_id = video_obj.tags.values_list("id", flat=True)

        # Get all text from the database with same tags
        similar_videos = Video.objects.filter(tags__in=video_tags_id).exclude(
            id=video_obj.id
        )
        similar_videos = similar_videos.annotate(similar_tags=Count("tags")).order_by(
            "similar_tags"
        )

        # serialize data
        similar_video_serializer = VideoCreateSerializer(
            similar_videos, many=True, context={"request": request}
        )

        return Response({"results": similar_video_serializer.data})

    elif target_content == models.Design:
        try:
            design_obj = Design.objects.get(id=content_id)
        except Design.DoesNotExist:
            return Response({"results": []}, status=200)

        # Get the tags of the design obj
        design_tags_id = design_obj.tags.values_list("id", flat=True)

        # Get all other designs with similar tags
        similar_designs = Design.objects.filter(tags__in=design_tags_id).exclude(
            id=design_obj.id
        )
        similar_designs = similar_designs.annotate(similar_tags=Count("tags")).order_by(
            "similar_tags"
        )

        # serialize the data
        similar_design_serializer = DesignSerializer(
            similar_designs, many=True, context={"request": request}
        )

        return Response({"results": similar_design_serializer.data}, status=200)

    return Response({"error": "invalid content type provided"}, status=400)


@api_view(["GET"])
def subsequent_episodes(request, content_type, season_id):
    """Returns a list of episodes related to the season object

    Args:
        content_type (str): model
        season_id (int): id of the episode selected to get related season
    """

    content_type_mapping = {"anime": models.Anime, "story": models.WrittenStory}

    target_content = content_type_mapping.get(content_type)
    try:
        season_obj = Season.objects.get(id=season_id)

    except Season.DoesNotExist:
        return Response({"error": "Invalid season obj provided"})

    if target_content == models.Anime:

        anime_season_result = season_obj.anime_season.all()

        # serialize the data
        anime_season_serializer = AnimeSerializer(
            anime_season_result, many=True, context={"request": request}
        )
        return Response({"results": anime_season_serializer.data}, status=200)

    elif target_content == models.WrittenStory:
        story_season_results = season_obj.writtenstory_season.all()

        # serialize the data
        story_season_serializer = StorySerializer(
            story_season_results, many=True, context={"request": request}
        )
        return Response({"results": story_season_serializer.data}, status=200)
    return Response({"error": "invalid content type provided"}, status=400)


class RecommdationSystem(APIView):
    pagination_class = RecommendationPagination

    def get(self, request, *args, **kwargs):

        user = request.user
        combined_data = None
        paginator = self.pagination_class()
        count = 0
        # get user profile
        try:
            user_profile = CreatorProfile.objects.get(creator=user)
        except CreatorProfile.DoesNotExist:
            return Response({"error": "resource not found"})

            # get user interests
        user_interest = user_profile.interests.all()

        interests = [i.name for i in user_interest]

        # to keep track of the video data from skits so that the same data won't be appended by videography
        data_state = []

        for interest in interests:
            if interest == "skits":
                # get data from textcontent and video content model
                # filter them by lastest post (release_date)
                text_data = Text.objects.all().order_by("-release_date")

                # combine queryset to paginate
                combined_data = (
                    text_data
                    if not combined_data
                    else list(combined_data) + list(text_data)
                )

                video_data = Video.objects.all().order_by("-release_date")

                # combine queryset to paginate
                combined_data = (
                    video_data
                    if not combined_data
                    else list(combined_data) + list(video_data)
                )

                data_state.append("skits")

            if interest == "videography" and "skits" not in data_state:

                video_data = Video.objects.all().order_by("-release_date")
                # combine queryset to paginate
                combined_data = (
                    video_data
                    if not combined_data
                    else list(combined_data) + list(video_data)
                )

            if interest == "animation":
                # get data from anime model
                # filter the returned data by latest post (release data)
                animation_data = Anime.objects.all().order_by("-release_date")

                # combine queryset to paginate
                combined_data = (
                    animation_data
                    if not combined_data
                    else list(combined_data) + list(animation_data)
                )
                # count += animation_data.count()

            if interest == "writtenstories":
                # data data from writtenstories model
                # filter the returned data by latest post (release_date)
                written_stories = WrittenStory.objects.all().order_by("-release_date")

                # combine queryset to paginate
                combined_data = (
                    written_stories
                    if not combined_data
                    else list(combined_data) + list(written_stories)
                )

        # paginate the combined querset
        page = paginator.paginate_queryset(combined_data, request, view=self)

        # serialize the paginated data
        if page is not None:
            # Determine the serializer to use for each object
            serialized_data = []
            for obj in page:
                if isinstance(obj, Anime):
                    serialized_data.append(
                        AnimeSerializer(obj, context={"request": request}).data
                    )
                elif isinstance(obj, Text):
                    serialized_data.append(
                        TextCreateSerializer(obj, context={"request": request}).data
                    )
                elif isinstance(obj, Video):
                    serialized_data.append(
                        VideoCreateSerializer(obj, context={"request": request}).data
                    )
                elif isinstance(obj, WrittenStory):
                    serialized_data.append(
                        StoryCreateSerializer(obj, context={"request": request}).data
                    )

            # Get the paginated response witth the total count
            total_count = len(combined_data)
            return paginator.get_paginated_response(serialized_data, total_count)

        return Response({"message": []})

    def paginate_queryset(self, queryset, request, view=None):
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view)
        return paginated_queryset


class PhotographyCreateListAPIView(generics.ListCreateAPIView):
    """
    list and create design/illustration object
    """

    queryset = Photography.objects.all()
    serializer_class = PhotographyCreateSerializer

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serailizer = DesignSerializer(queryset, many=True, context={"request": request})
    #     return Response({"result": serailizer.data}, status=status.HTTP_200_OK)


class PhotographyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve: pk
    Update: pk
    Delete: pk
    """

    # queryset = Design.objects.all()
    serializer_class = PhotographyDetailSerializer

    def get_queryset(self):
        """
        Can be used to return objects filtered by either the user or the object's slug itself. It returns all items by default if no query_params is provided in the url
        """

        queryset = Photography.objects.all()

        user_id = self.request.query_params.get("id")
        design_slug = self.request.query_params.get("slug")

        if user_id is not None:
            queryset = queryset.filter(creator=user_id)
        elif design_slug is not None:
            queryset = queryset.filter(slug=design_slug)
        return queryset

    def delete(self, request, *args, **kwargs):
        design = self.get_object()
        req_user_prof = CreatorProfile.objects.get(creator=request.user)

        if design.creator != req_user_prof:
            return Response(
                {"detail": "You do not have the permission to delete this content"}
            )

        return self.destroy(request, *args, **kwargs)


@api_view
def comment_on_post(request):
    pass
