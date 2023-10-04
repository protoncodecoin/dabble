from rest_framework import serializers

from django.utils.text import slugify

from .models import Series, Story, Anime
from comment_system.serializers import CommentSerializer

from django.contrib.contenttypes.models import ContentType

from .models import Series, Season
from comment_system.models import Comment


class CreatorInlineSerializer(serializers.Serializer):
    "Serialize data related to creator profile"
    company_name = serializers.CharField(read_only=True)
    company_description = serializers.CharField(read_only=True)
    company_website = serializers.URLField(read_only=True)
    creator_logo = serializers.ImageField(read_only=True)


class ContactInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="follow-detail",
        lookup_field="pk",
    )


class SeriesSerializer(serializers.ModelSerializer):
    """Serialize the Series Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="series-detail", lookup_field="pk"
    )
    slug = serializers.SerializerMethodField()
    creator = serializers.ReadOnlyField(source="creator.username")
    likes = serializers.ReadOnlyField(source="likes.count")

    class Meta:
        """Meta class for Series Serializer"""

        model = Series
        fields = [
            "url",
            "pk",
            "creator",
            "series_name",
            "slug",
            "series_poster",
            "synopsis",
            "likes",
        ]
        extra_kwargs = {
            "slug": {"write_only": True},
        }

    def get_slug(self, obj):
        """Generate a method to generate the slug field"""
        return slugify(obj.series_name)


class SeriesDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="creator", read_only=True)
    creator = serializers.ReadOnlyField(source="creator.username")
    comments = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField(source="likes.count")
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = [
            "pk",
            "creator",
            "series_name",
            "synopsis",
            "start_date",
            "end_date",
            "user_has_liked",
            "total_likes",
            "likes",
            "liked_user_names",
            "owner",
            "comments",
        ]

    def get_user_has_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(pk=user.pk).exists()

    def get_liked_user_names(self, obj):
        liked_users = obj.likes.all()
        liked_usernames = [user.username for user in liked_users]
        return liked_usernames

    def get_comments(self, obj):
        target_content_type = ContentType.objects.get_for_model(Series)
        comments = Comment.objects.filter(
            target_ct=target_content_type, target_id=obj.id
        )

        all_comments = {comment.comment: comment.user.email for comment in comments}

        return all_comments


class StorySerializer(serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="story-detail", lookup_field="pk"
    )
    series = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season = serializers.ReadOnlyField(source="season.season_number")

    class Meta:
        """Meta class of Story Serializer"""

        model = Story
        fields = [
            "pk",
            "url",
            "series",
            "episode_number",
            "episode_title",
            "likes",
            "season",
        ]


class StoryDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator")
    series = serializers.ReadOnlyField(source="series.series_name")
    user_has_liked = serializers.SerializerMethodField()
    likes = serializers.ReadOnlyField(source="likes.count")
    comments = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()
    season = serializers.ReadOnlyField(source="season.season_number")

    class Meta:
        model = Story
        fields = [
            "pk",
            "series",
            "season",
            "episode_number",
            "episode_title",
            "episode_release_date",
            "user_has_liked",
            "likes",
            "liked_user_names",
            "description",
            "content",
            "owner",
            "comments",
        ]

    def get_user_has_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(pk=user.pk).exists()

    def get_liked_user_names(self, obj):
        liked_users = obj.likes.all()
        liked_usernames = [user.username for user in liked_users]
        return liked_usernames

    def get_comments(self, obj):
        target_content_type = ContentType.objects.get_for_model(Story)
        comments = Comment.objects.filter(
            target_ct=target_content_type, target_id=obj.id
        )

        all_comments = {comment.comment: comment.user.email for comment in comments}
        return all_comments


class AnimeSerializer(serializers.ModelSerializer):
    """A Model Serializer for Anime Model"""

    creator = serializers.ReadOnlyField(source="series.creator.company_name")
    url = serializers.HyperlinkedIdentityField(
        view_name="anime-detail", lookup_field="pk"
    )
    series = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")

    class Meta:
        """Meta class for Anime Serializer"""

        model = Anime
        fields = [
            "pk",
            "url",
            "series",
            "episode_title",
            "episode_number",
            "likes",
            "thumbnail",
            "creator",
        ]


class AnimeDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator")
    comments = serializers.SerializerMethodField()
    series = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            "pk",
            "series",
            "episode_number",
            "episode_title",
            "episode_release_date",
            "user_has_liked",
            "publish",
            "thumbnail",
            "likes",
            "liked_user_names",
            "file",
            "comments",
            "owner",
        ]

    def get_user_has_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(pk=user.pk).exists()

    def get_liked_user_names(self, obj):
        liked_users = obj.likes.all()
        liked_usernames = [user.username for user in liked_users]
        return liked_usernames

    def get_comments(self, obj):
        target_content_type = ContentType.objects.get_for_model(Anime)
        comments = Comment.objects.filter(
            target_ct=target_content_type, target_id=obj.id
        )

        # all_comments = [comment.comment for comment in comments]
        all_comments = {comment.comment: comment.user.email for comment in comments}
        return all_comments
