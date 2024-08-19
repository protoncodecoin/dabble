from anime_api import models
from rest_framework import serializers


class SimpleAnimeSerializer(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(
        source="series.creator.creator.username"
    )

    class Meta:
        model = models.Anime
        fields = [
            "id",
            "slug",
            "episode_title",
            "thumbnail",
            "typeof",
            "creator_username",
        ]


class SimpleAnimeSerializerWithTrends(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(
        source="series.creator.creator.username"
    )
    count_likes = serializers.IntegerField()

    class Meta:
        model = models.Anime
        fields = [
            "id",
            "slug",
            "episode_title",
            "thumbnail",
            "typeof",
            "creator_username",
            "count_likes",
        ]


class SimpleWrittenStory(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(
        source="series.creator.creator.username"
    )

    class Meta:
        model = models.WrittenStory
        fields = [
            "id",
            "slug",
            "episode_title",
            "thumbnail",
            "typeof",
            "creator_username",
        ]


class SimpleDesignSerializer(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(source="creator.creator.username")

    class Meta:
        model = models.Design
        fields = [
            "id",
            "slug",
            "title",
            "illustration",
            "typeof",
            "creator",
            "creator_username",
        ]


class SimpleVideoSerializer(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(source="creator.creator.username")

    class Meta:
        model = models.Video
        fields = [
            "id",
            "slug",
            "title",
            "thumbnail",
            "typeof",
            "creator_username",
        ]


class SimpleTextSerializer(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(source="creator.creator.username")

    class Meta:
        model = models.Video
        fields = [
            "id",
            "slug",
            "title",
            "thumbnail",
            "typeof",
            "creator_username",
        ]


class SimplePhotographySerializer(serializers.ModelSerializer):
    """
    Simple serializer to serialize data in django views
    """

    creator_username = serializers.ReadOnlyField(source="creator.creator.username")

    class Meta:
        model = models.Photography
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "typeof",
            "creator_username",
        ]
