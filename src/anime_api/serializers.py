from rest_framework import serializers

from django.utils.text import slugify

from .models import Series, Story, Anime
from comment_system.serializers import CommentSerializer


class CreatorRelSerializer(serializers.Serializer):
    "Serialize data related to creator profile"
    company_name = serializers.CharField(read_only=True)
    company_description = serializers.CharField(read_only=True)
    company_website = serializers.URLField(read_only=True)
    creator_logo = serializers.ImageField(read_only=True)


class SeriesSerializer(serializers.ModelSerializer):
    """Serialize the Series Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="series-detail", lookup_field="pk"
    )
    slug = serializers.SerializerMethodField()
    # owner = CreatorRelSerializer(source="creator.user_created")

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
            # "start_date",
            # "end_date",
        ]
        extra_kwargs = {
            "slug": {"write_only": True},
        }

    def get_slug(self, obj):
        """Generate a method to generate the slug field"""
        return slugify(obj.series_name)


class SeriesDetailSerializer(serializers.ModelSerializer):
    owner = CreatorRelSerializer(source="creator.creator_profile")

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
            # "comment",
        ]


class StorySerializer(serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="story-detail", lookup_field="pk"
    )

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
    owner = CreatorRelSerializer(source="series.creator.creator_profile")

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
            "publish",
            "owner",
        ]


class AnimeSerializer(serializers.ModelSerializer):
    """A Model Serializer for Anime Model"""

    creator = serializers.ReadOnlyField(source="series.creator.username")
    url = serializers.HyperlinkedIdentityField(
        view_name="anime-detail", lookup_field="pk"
    )

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
    owner = CreatorRelSerializer(source="series.creator.creator_profile")

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
        ]
