from rest_framework import serializers

from django.utils.text import slugify

from .models import Series, Story, Anime
from comment_system.serializers import CommentSerializer


class CreatorInlineSerializer(serializers.Serializer):
    "Serialize data related to creator profile"
    company_name = serializers.CharField(read_only=True)
    company_description = serializers.CharField(read_only=True)
    company_website = serializers.URLField(read_only=True)
    creator_logo = serializers.ImageField(read_only=True)


class CommentInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="comment-detail", lookup_field="pk", read_only=True
    )
    comment = serializers.TimeField(read_only=True)
    created = serializers.DateTimeField(read_only=True)


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
    # likes = serializers.ReadOnlyField(source="creator.")

    class Meta:
        """Meta class for Series Serializer"""

        model = Series
        fields = [
            # "owner",
            "url",
            "pk",
            "creator",
            "series_name",
            "slug",
            "series_poster",
            "synopsis",
        ]
        extra_kwargs = {
            "slug": {"write_only": True},
        }

    def get_slug(self, obj):
        """Generate a method to generate the slug field"""
        return slugify(obj.series_name)


class SeriesDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="creator.creator_profile")
    creator = serializers.ReadOnlyField(source="creator.username")
    comments = CommentInlineSerializer(
        source="creator.comments.all", many=True, read_only=True
    )

    class Meta:
        model = Series
        fields = [
            "pk",
            "creator",
            "series_name",
            "synopsis",
            "start_date",
            "end_date",
            "owner",
            "comments",
        ]


class StorySerializer(serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="story-detail", lookup_field="pk"
    )
    series = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        """Meta class of Story Serializer"""

        model = Story
        fields = [
            "pk",
            "url",
            "series",
            "episode_number",
            "episode_title",
            # "description",
            # "episode_release_date",
            # "content",
            # "publish",
        ]


class StoryDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator.creator_profile")
    series = serializers.ReadOnlyField(source="series.series_name")
    comments = CommentInlineSerializer(
        source="series.creator.comments.all", many=True, read_only=True
    )

    class Meta:
        model = Story
        fields = [
            "pk",
            "series",
            "episode_number",
            "episode_title",
            "description",
            "episode_release_date",
            "content",
            "owner",
            "comments",
        ]


class AnimeSerializer(serializers.ModelSerializer):
    """A Model Serializer for Anime Model"""

    creator = serializers.ReadOnlyField(source="series.creator.username")
    url = serializers.HyperlinkedIdentityField(
        view_name="anime-detail", lookup_field="pk"
    )
    series = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        """Meta class for Anime Serializer"""

        model = Anime
        fields = [
            "pk",
            "url",
            "series",
            "episode_number",
            "episode_title",
            # "episode_release_date",
            # "publish",
            "thumbnail",
            "file",
            "creator",
        ]


class AnimeDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator.creator_profile")
    comments = CommentInlineSerializer(
        source="series.creator.comments.all", many=True, read_only=True
    )
    series = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        model = Anime
        fields = [
            "pk",
            "series",
            "episode_number",
            "episode_title",
            "episode_release_date",
            "publish",
            "thumbnail",
            "file",
            "owner",
            "comments",
        ]
