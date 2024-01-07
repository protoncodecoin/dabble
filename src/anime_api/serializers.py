from wsgiref import validate
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from taggit.serializers import (
    TaggitSerializer,
    TagListSerializerField,
)
from taggit.models import Tag

from .models import (
    Series,
    Story,
    Anime,
    Season,
)

from comment_system.models import Comment
from users_api.models import CreatorProfile

from .utils import media_renamer, media_renamer, video_file_checker


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


class SeriesSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serialize the Series Model"""

    tags = TagListSerializerField()
    url = serializers.HyperlinkedIdentityField(
        view_name="animes:series-detail", lookup_field="pk"
    )
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
            "series_poster",
            "synopsis",
            "likes",
            "tags",
        ]

        extra_kwargs = {
            "slug": {"write_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if request.user.is_creator:
            user = request.user.creator_profile
            series_name = self.validated_data.get("series_name")
            series_poster = self.validated_data.get("series_poster")
            synopsis = self.validated_data.get("synopsis")

            tags = self.validated_data["tags"][0]  # expected data ["pen,pencil,book"]

            tags = tags.split(",")
            tags = [tag.strip() for tag in tags]

            tag_list = []  # creating or getting tags from names
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tag_list.append(tag)

            new_series = Series.objects.create(
                creator=user,
                series_name=series_name,
                synopsis=synopsis,
                series_poster=series_poster,
            )
            new_series.tags.add(*tags)

            return new_series
        raise serializers.ValidationError("You do not have the permission to create")


class SeriesDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="creator", read_only=True)
    creator = serializers.ReadOnlyField(source="creator.username")
    comments = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField(source="likes.count")
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Series
        fields = [
            "pk",
            "creator",
            "series_name",
            "synopsis",
            "series_poster",
            "start_date",
            "end_date",
            "user_has_liked",
            "total_likes",
            "likes",
            "liked_user_names",
            "owner",
            "comments",
            "tags",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request.user.is_creator:
            if request.user == instance.creator:
                tags_data = validated_data.pop("tags", None)
                if tags_data:
                    tags_list = tags_data[0].split(
                        ","
                    )  # Assuming tags are sent as ["pen,pencil,book"]
                    tags_list = [tag.strip() for tag in tags_list]

                    tag_instances = []  # To hold the tag instances
                    for tag_name in tags_list:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag_instances.append(tag)

                    instance.tags.set(tag_instances)

                return super().update(instance, validated_data)

            raise serializers.ValidationError(
                "You do not have the permission to modify this resources."
            )
        raise serializers.ValidationError(
            "You do not have required permission to take modify this resources."
        )

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


class StorySerializer(TaggitSerializer, serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="animes:story-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season_number = serializers.ReadOnlyField(source="season.season_number")
    season_id = serializers.ReadOnlyField(source="season.id")
    tags = TagListSerializerField()

    class Meta:
        """Meta class of Story Serializer"""

        model = Story
        fields = [
            "pk",
            "url",
            "series",
            "series_name",
            "episode_number",
            "episode_title",
            "likes",
            "season_id",
            "season_number",
            "tags",
        ]


class StoryCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="animes:story-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season_number = serializers.ReadOnlyField(source="season.season_number")
    tags = TagListSerializerField()

    class Meta:
        """Meta class of Story Serializer"""

        model = Story
        fields = [
            "pk",
            "url",
            "series",
            "series_name",
            "episode_number",
            "episode_title",
            "thumbnail",
            "description",
            "content",
            "tags",
            "likes",
            "season",
            "season_number",
        ]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user.creator_profile
        creator = data["series"].creator

        if user == creator:
            if data["series"] == data["season"].series:
                qs = Story.objects.filter(
                    series=data["series"],
                    season=data["season"],
                    episode_title=data["episode_title"],
                    episode_number=data["episode_number"],
                )
                if qs.exists():
                    total_num_episodes = Story.objects.filter(
                        series=data["series"], season=data["season"]
                    ).count()
                    data["episode_number"] += (
                        total_num_episodes if total_num_episodes else 1
                    )
                    return data

                return data
            raise serializers.ValidationError(
                "ID of series does not match season_series"
            )
        raise serializers.ValidationError("You don't have permission")

    def create(self, validated_data):
        series_id = validated_data.get("series")
        season_id = validated_data.get("season")
        episode_number = validated_data.get("episode_number")
        episode_title = validated_data["episode_title"]
        description = validated_data.get("description", "")
        thumbnail = validated_data.get("thumbnail")
        content = validated_data["content"]
        tags = self.validated_data["tags"]
        split_tags = tags[0].split(",")
        strip_tags = [tag.strip() for tag in split_tags]

        tag_list = []
        for tag_name in strip_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)

        if validated_data.get("thumbnail"):
            series_name = validated_data.get("series").series_name
            season_number = validated_data.get("season").season_number
            file_type = validated_data.get("thumbnail").name.split(".")[-1]

            generated_thumbnail_name = media_renamer(
                series_name, season_number, episode_number, file_type
            )

            thumbnail.name = generated_thumbnail_name

        new_story_obj = Story.objects.create(
            series=series_id,
            season=season_id,
            episode_number=episode_number,
            episode_title=episode_title,
            content=content,
            description=description,
            thumbnail=thumbnail,
        )
        new_story_obj.tags.add(*tag_list)
        return new_story_obj


class StoryDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator", read_only=True)
    series_name = serializers.ReadOnlyField(source="series.series_name")
    user_has_liked = serializers.SerializerMethodField()
    likes = serializers.ReadOnlyField(source="likes.count")
    comments = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()
    season_number = serializers.ReadOnlyField(source="season.season_number")
    tags = TagListSerializerField()

    class Meta:
        model = Story
        fields = [
            "pk",
            "series",
            "series_name",
            "season_number",
            "season",
            "episode_number",
            "episode_title",
            "episode_release_date",
            "user_has_liked",
            "likes",
            "liked_user_names",
            "description",
            "content",
            "thumbnail",
            "owner",
            "comments",
            "tags",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request.user.is_creator:
            user_profile = CreatorProfile.objects.get(creator=request.user)
            if user_profile == instance.series.creator:
                tags_data = validated_data.pop("tags", None)
                if tags_data:
                    tags_list = tags_data[0].split(
                        ","
                    )  # Assuming tags are sent as ["pen,pencil,book"]
                    tags_list = [tag.strip() for tag in tags_list]

                    tag_instances = []  # To hold the tag instances
                    for tag_name in tags_list:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag_instances.append(tag)

                    instance.tags.set(tag_instances)

                req_thumbnail = validated_data.get("thumbnail")

                if req_thumbnail:
                    story_name = instance.series.series_name
                    season = instance.season.season_number
                    episode_number = instance.episode_number
                    file_type = req_thumbnail.name.split(".")[-1]

                    generated_thumbnail_name = media_renamer(
                        story_name, season, episode_number, file_type
                    )

                    req_thumbnail.name = generated_thumbnail_name

                return super().update(instance, validated_data)

            raise serializers.ValidationError(
                "You do not have the required permission to modify this resources."
            )
        raise serializers.ValidationError("You are not the creator of this file.")

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


class AnimeSerializer(TaggitSerializer, serializers.ModelSerializer):
    """A Model Serializer for Anime Model"""

    creator = serializers.ReadOnlyField(source="series.creator.company_name")
    url = serializers.HyperlinkedIdentityField(
        view_name="animes:anime-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season_number = serializers.ReadOnlyField(
        source="season.season_number", read_only=True
    )
    tags = TagListSerializerField()

    class Meta:
        """Meta class for Anime Serializer"""

        model = Anime
        fields = [
            "pk",
            "url",
            "series_name",
            "series",
            "episode_title",
            "episode_number",
            "description",
            "likes",
            "anime_thumbnail",
            "video_file",
            "season",
            "season_number",
            "creator",
            "tags",
        ]


class AnimeCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Anime
        fields = [
            "pk",
            "series",
            "season",
            "episode_number",
            "episode_title",
            "description",
            "video_file",
            "tags",
            "anime_thumbnail",
        ]

    def validate(self, data):
        request = self.context.get("request")
        req_series = data.get("series")

        if request.user.is_creator and req_series.creator:
            # check if series exist
            # check if the user created the series
            series_obj = Series.objects.get(id=req_series.id)
            creator_obj = CreatorProfile.objects.get(creator=request.user)

            if creator_obj == series_obj.creator:
                try:
                    # check if the series is related to the season
                    if series_obj.season.get(id=data.get("season").id):
                        pass
                except Season.DoesNotExist:
                    # will use logger here to log error just in case
                    raise serializers.ValidationError("Season Id is invalid.")

                # check if there is an exiting episode
                episode_number = data.get("episode_number")
                if episode_number:
                    anime_obj = Anime.objects.filter(
                        episode_number=episode_number
                    ).first()

                    if anime_obj:
                        raise serializers.ValidationError(
                            "Episode number already exist."
                        )

                    sent_video_type = data.get("video_file").name.split(".")[-1]

                    if video_file_checker(sent_video_type):
                        return data

                    raise serializers.ValidationError("File Format not supported.")

                raise serializers.ValidationError("Episode number is required.")

            raise serializers.ValidationError(
                "You do not have the permission to modify this file."
            )

        raise serializers.ValidationError("You don't have permission to create")

    def create(self, validated_data):
        series_id = validated_data.get("series")
        season_id = validated_data.get("season")
        episode_title = validated_data.get("episode_title")
        episode_number = validated_data.get("episode_number")
        description = validated_data.get("description")
        thumbnail = validated_data.get("anime_thumbnail")
        file = validated_data.get("video_file")
        tags = validated_data.get("tags")
        split_tags = tags[0].split(",")
        strip_tags = [tag.strip() for tag in split_tags]

        tag_objs = []

        for tag_name in strip_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objs.append(tag)

        # Rename file name to series name + season number+ episode number
        req_series_name = validated_data.get("series").series_name
        req_season_number = validated_data.get("season").season_number
        req_episode_number = validated_data.get("episode_number")

        video_file_type = file.name.split(".")[-1]

        if thumbnail:
            thumbnail_type = thumbnail.name.split(".")[-1]

            generated_thumbnail_name = media_renamer(
                req_series_name, req_season_number, req_episode_number, thumbnail_type
            )
            thumbnail.name = generated_thumbnail_name

        generated_file_name = media_renamer(
            req_series_name, req_season_number, req_episode_number, video_file_type
        )
        file.name = generated_file_name

        new_anime_obj = Anime.objects.create(
            series=series_id,
            season=season_id,
            episode_title=episode_title,
            episode_number=episode_number,
            description=description,
            anime_thumbnail=thumbnail,
            video_file=file,
        )
        new_anime_obj.tags.add(*tag_objs)

        return new_anime_obj


class AnimeDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator", read_only=True)
    comments = serializers.SerializerMethodField()
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Anime
        fields = [
            "pk",
            "series",
            "series_name",
            "episode_number",
            "episode_title",
            "season",
            "episode_release_date",
            "user_has_liked",
            "publish",
            "tags",
            "anime_thumbnail",
            "likes",
            "liked_user_names",
            "video_file",
            "comments",
            "owner",
            "description",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request.user.is_creator:
            req_creator = CreatorProfile.objects.get(creator=request.user)
            if req_creator == instance.series.creator:
                tags_data = validated_data.pop("tags", None)
                if tags_data:
                    tags_list = tags_data[0].split(
                        ","
                    )  # Assuming tags are sent as ["pen,pencil,book"]
                    tags_list = [tag.strip() for tag in tags_list]

                    tag_instances = []  # To hold the tag instances
                    for tag_name in tags_list:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag_instances.append(tag)

                    instance.tags.set(tag_instances)

                if validated_data.get("video_file"):
                    sent_video_type = validated_data.get("video_file").name.split(".")[
                        -1
                    ]

                    if video_file_checker(sent_video_type):
                        req_series_name = instance.series.series_name
                        req_season_number = instance.season.season_number
                        req_episode_number = instance.episode_number

                        generated_file_name = media_renamer(
                            req_series_name,
                            req_season_number,
                            req_episode_number,
                            sent_video_type,
                        )

                        validated_data.get(
                            "video_file"
                        ).name = f"{generated_file_name}.{sent_video_type}"

                if validated_data.get("anime_thumbnail"):
                    sent_thumbnail_type = validated_data.get(
                        "anime_thumbnail"
                    ).name.split(".")[-1]

                    generated_file_name = media_renamer(
                        req_series_name,
                        req_season_number,
                        req_episode_number,
                        sent_thumbnail_type,
                    )
                    validated_data.get(
                        "anime_thumbnail"
                    ).name = f"{generated_file_name}.{sent_thumbnail_type}"

                return super().update(instance, validated_data)

            raise serializers.ValidationError(
                "You do not have the permission to modify this resources."
            )
        raise serializers.ValidationError(
            "You do not have required permission to take modify this resources."
        )

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
        all_comments = {comment.comment: comment.user.email for comment in comments}
        return all_comments


class SeasonSerializer(serializers.ModelSerializer):
    series_name = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        model = Season
        fields = [
            "pk",
            "series_name",
            "series",
            "season_number",
            "release_date",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request.user.is_creator:
            user_obj = CreatorProfile.objects.get(creator=request.user)
            if user_obj == instance.series.creator:
                return super().update(instance=instance, validated_data=validated_data)
            raise serializers.ValidationError(
                "You don't have the permission to modify this resources"
            )
        raise serializers.ValidationError(
            "You don't have the permission to access this file."
        )


class SeasonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = [
            "pk",
            "series",
            "season_number",
            "release_date",
        ]

    def validate(self, data):
        request = self.context.get("request")

        # if creator == user:
        if request.user.is_creator:
            creator = data["series"].creator
            user = request.user.creator_profile
            if creator == user:
                qs = Season.objects.filter(
                    series=data["series"], season_number=data["season_number"]
                ).exists()
                if qs:
                    raise serializers.ValidationError(
                        f"Season object with id of {data['season_number']} exists"
                    )
                else:
                    return data
            else:
                raise serializers.ValidationError("You can edit this object")

    def create(self, validated_data):
        series_id = validated_data.get("series")
        season_number = validated_data.get("season_number")
        return Season.objects.create(series=series_id, season_number=season_number)
