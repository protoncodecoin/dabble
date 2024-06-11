from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from taggit.serializers import (
    TaggitSerializer,
    TagListSerializerField,
)
from taggit.models import Tag

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
from users_api.models import CreatorProfile

from .utils import media_renamer, video_file_checker


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
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )
    seasons = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="season-detail",
        source="series.season.all",
    )

    class Meta:
        """Meta class for Series Serializer"""

        model = Series
        fields = [
            "url",
            "pk",
            "slug",
            "creator",
            "series_name",
            "series_poster",
            "synopsis",
            "likes",
            "tags",
            "seasons",
            "start_date",
            "end_date",
            "typeof",
        ]

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
    user_has_liked = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )
    season = serializers.HyperlinkedIdentityField(
        view_name="animes:season-detail",
        read_only=True,
        many=True,
    )

    class Meta:
        model = Series
        fields = [
            "pk",
            "slug",
            "creator",
            "series_name",
            "synopsis",
            "series_poster",
            "start_date",
            "end_date",
            "user_has_liked",
            "likes",
            "owner",
            "comments",
            "tags",
            "season",
            "typeof",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request.user.is_creator:
            query_profile = CreatorProfile.objects.get(creator=request.user)
            if query_profile == instance.creator:
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

    def get_comments(self, obj):
        target_content_type = ContentType.objects.get_for_model(Series)
        comments = Comment.objects.filter(
            content_type=target_content_type, object_id=obj.id
        )

        all_comments = {comment.text: comment.user.user.email for comment in comments}

        # all_comments = {"message": "howl"}

        return all_comments


class StorySerializer(TaggitSerializer, serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="animes:story-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    season_number = serializers.ReadOnlyField(source="season.season_number")
    creative_type = serializers.ReadOnlyField(source="season.obj_type")
    season_id = serializers.ReadOnlyField(source="season.id")
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        """Meta class of Story Serializer"""

        model = WrittenStory
        fields = [
            "pk",
            "url",
            "slug",
            "series",
            "series_name",
            "episode_number",
            "episode_title",
            "likes",
            "season_id",
            "season_number",
            "creative_type",
            "tags",
            "thumbnail",
            "release_date",
            "typeof",
        ]


class StoryCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="animes:story-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )
    season_number = serializers.ReadOnlyField(source="season.season_number")
    tags = TagListSerializerField()

    class Meta:
        """Meta class of Story Serializer"""

        model = WrittenStory
        fields = [
            "pk",
            "url",
            "slug",
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
            "release_date",
            "typeof",
        ]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user.creator_profile
        creator = data["series"].creator

        if user == creator:
            if data["series"] == data["season"].series:
                qs = WrittenStory.objects.filter(
                    series=data["series"],
                    season=data["season"],
                    episode_title=data["episode_title"],
                    episode_number=data["episode_number"],
                )
                if qs.exists():
                    total_num_episodes = WrittenStory.objects.filter(
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

        new_story_obj = WrittenStory.objects.create(
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
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )
    comments = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    season_number = serializers.ReadOnlyField(source="season.season_number")

    tags = TagListSerializerField()

    class Meta:
        model = WrittenStory
        fields = [
            "pk",
            "slug",
            "series",
            "series_name",
            "season_number",
            "season",
            "episode_number",
            "episode_title",
            "release_date",
            "user_has_liked",
            "likes",
            "description",
            "content",
            "thumbnail",
            "owner",
            "comments",
            "tags",
            "typeof",
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
        target_content_type = ContentType.objects.get_for_model(WrittenStory)
        comments = Comment.objects.filter(
            content_type=target_content_type, object_id=obj.id
        )

        all_comments = {comment.comment: comment.user.email for comment in comments}
        return all_comments


class StoryFavoriteSerializer(serializers.ModelSerializer):
    """
    Serializers user favorites
    """

    episode_url = serializers.HyperlinkedIdentityField(view_name="animes:story-detail")
    series_name = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        model = WrittenStory
        fields = [
            "series_name",
            "episode_title",
            "episode_number",
            "thumbnail",
            "episode_url",
        ]


class SeriesFavoriteSerializer(serializers.ModelSerializer):
    """
    Serializers user favorites
    """

    episode_url = serializers.HyperlinkedIdentityField(view_name="animes:series-detail")
    series_name = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        model = Series
        fields = [
            "series_name",
            "series_poster",
            "episode_url",
        ]


class AnimeSerializer(TaggitSerializer, serializers.ModelSerializer):
    """A Model Serializer for Anime Model"""

    creator = serializers.ReadOnlyField(source="series.creator.creator.username")
    url = serializers.HyperlinkedIdentityField(
        view_name="animes:anime-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )
    season_number = serializers.ReadOnlyField(
        source="season.season_number", read_only=True
    )
    tags = TagListSerializerField()

    class Meta:
        """Meta class for Anime Serializer"""

        model = Anime
        fields = [
            "pk",
            "slug",
            "url",
            "series_name",
            "series",
            "episode_title",
            "episode_number",
            "description",
            "likes",
            "thumbnail",
            # "video_file",
            "season",
            "season_number",
            "creator",
            "tags",
            "typeof",
        ]


class AnimeCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Anime
        fields = [
            "pk",
            "slug",
            "series",
            "season",
            "episode_number",
            "episode_title",
            "description",
            "video_file",
            "tags",
            "thumbnail",
            "likes",
            "typeof",
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
        thumbnail = validated_data.get("thumbnail")
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
            thumbnail=thumbnail,
            video_file=file,
        )
        new_anime_obj.tags.add(*tag_objs)

        return new_anime_obj


class AnimeFavoriteSerializer(serializers.ModelSerializer):
    """
    Serializers user favorites
    """

    episode_url = serializers.HyperlinkedIdentityField(view_name="animes:anime-detail")
    series_name = serializers.ReadOnlyField(source="series.series_name")

    class Meta:
        model = Anime
        fields = [
            "series_name",
            "episode_title",
            "episode_number",
            "thumbnail",
            "episode_url",
        ]


class AnimeDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator", read_only=True)
    comments = serializers.SerializerMethodField()
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )
    user_has_liked = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    # favorited_urls = serializers.HyperlinkedRelatedField(
    #     view_name="animes:favorite-detail", read_only=True
    # )

    class Meta:
        model = Anime
        fields = [
            "pk",
            "slug",
            "series",
            "series_name",
            "episode_number",
            "episode_title",
            "season",
            "release_date",
            "user_has_liked",
            "publish",
            "tags",
            "likes",
            "description",
            "thumbnail",
            "video_file",
            "comments",
            "owner",
            "favorited_by",
            "typeof",
            # "favorited_urls",
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

                req_series_name = instance.series.series_name
                req_season_number = instance.season.season_number
                req_episode_number = instance.episode_number

                if validated_data.get("video_file"):
                    sent_video_type = validated_data.get("video_file").name.split(".")[
                        -1
                    ]

                    if video_file_checker(sent_video_type):

                        generated_file_name = media_renamer(
                            req_series_name,
                            req_season_number,
                            req_episode_number,
                            sent_video_type,
                        )

                        validated_data.get("video_file").name = (
                            f"{generated_file_name}.{sent_video_type}"
                        )

                if validated_data.get("thumbnail"):
                    sent_thumbnail_type = validated_data.get("thumbnail").name.split(
                        "."
                    )[-1]

                    generated_file_name = media_renamer(
                        req_series_name,
                        req_season_number,
                        req_episode_number,
                        sent_thumbnail_type,
                    )
                    validated_data.get("thumbnail").name = (
                        f"{generated_file_name}.{sent_thumbnail_type}"
                    )

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

    def get_comments(self, obj):
        target_content_type = ContentType.objects.get_for_model(Anime)
        comments = Comment.objects.filter(
            content_type=target_content_type, object_id=obj.id
        )

        all_comments = {
            comment.created.strftime("%m/%d/%Y, %H:%M:%S"): [
                comment.user.user.email,
                comment.text,
            ]
            for comment in comments
            if comment.is_approved
        }

        return {"message": all_comments}


class SeasonSerializer(serializers.ModelSerializer):
    series_name = serializers.ReadOnlyField(source="series.series_name")
    url = serializers.HyperlinkedIdentityField(
        view_name="animes:season-detail", read_only=True
    )

    # episodes = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = [
            "pk",
            "url",
            "series_name",
            "series",
            "season_number",
            "release_date",
            "typeof",
            # "episodes",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request.user.is_creator:
            user_obj = CreatorProfile.objects.get(creator=request.user)
            if user_obj == instance.series.creator:
                # check if the episode of the validated data already exist in the data
                # Return an error it
                try:
                    Season.objects.filter(series=instance.series).get(
                        season_number=validated_data.get("season_number")
                    )
                except Season.DoesNotExist:
                    raise serializers.ValidationError("Episode Does not exist")

                return super().update(instance=instance, validated_data=validated_data)

            raise serializers.ValidationError(
                "You don't have the permission to modify this resources"
            )
        raise serializers.ValidationError(
            "You don't have the permission to access this file."
        )

    # def get_episodes(self, obj: Season):
    #     anime_instance = obj.anime_season.all()
    #     story_instance = obj.story_season.all()

    #     request = self.context.get("request")

    #     anime_serializer = AnimeSerializer(
    #         anime_instance, context={"request": request}
    #     ).data
    #     story_serializer = (
    #         StorySerializer(story_instance, context={"request": request}).data,
    #     )

    #     return [
    #         anime_serializer,
    #         story_serializer,
    #     ]


class SeasonCreateSerializer(serializers.ModelSerializer):
    # episodes = serializers.HyperlinkedIdentityField()

    class Meta:
        model = Season
        fields = [
            "pk",
            "series",
            "season_number",
            "release_date",
            "typeof",
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


class TextCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Text
        fields = [
            "id",
            "slug",
            "title",
            "synopsis",
            "content",
            "thumbnail",
            "creator",
            "tags",
            "release_date",
            "likes",
            "typeof",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        req_user = request.user

        if req_user.is_creator:
            try:
                creator_prof = CreatorProfile.objects.get(creator=req_user)

            except CreatorProfile.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
            if validated_data.get("creator") == creator_prof:
                if validated_data.get("thumbnail"):
                    title = validated_data.get("title")
                    extension = validated_data.get("thumbnail").name.split(".")[-1]
                    generated_name = f"{title}.{extension}"

                    validated_data.get("thumbnail").name = generated_name
                return super().create(validated_data)

            raise serializers.ValidationError("Invalid ID Provided")
        raise serializers.ValidationError("You do not have the permission")


class TextDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Text
        fields = [
            "id",
            "slug",
            "title",
            "content",
            "synopsis",
            "thumbnail",
            "release_date",
            "tags",
            "likes",
            "typeof",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        req_user = request.user

        if req_user.is_creator:
            try:
                req_creator = CreatorProfile.objects.get(creator=req_user)
            except CreatorProfile.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
            if req_creator == instance.creator:
                if validated_data.get("thumbnail"):
                    if validated_data.get("title"):
                        extension = validated_data.get("thumbnail").name.split(".")[-1]
                        title = validated_data.get("title")
                        generated_name = f"{title}.{extension}"
                        validated_data.get("thumbnaiil").name = generated_name
                return super().update(instance, validated_data)
            raise serializers.ValidationError(
                "You do not have the required permission."
            )
        raise serializers.ValidationError("You do not have the required permission.")


class DesignSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Design
        fields = [
            "creator",
            "id",
            "slug",
            "title",
            "synopsis",
            "illustration",
            "tags",
            "release_date",
            "likes",
            "typeof",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        req_user = request.user

        if req_user.is_creator:
            try:
                creator_prof = CreatorProfile.objects.get(creator=req_user)
            except CreatorProfile.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
            if validated_data.get("creator") == creator_prof:

                title = validated_data.get("title")
                extension = validated_data.get("illustration").name.split(".")[-1]
                generated_name = f"{title}.{extension}"
                validated_data.get("illustration").name = generated_name
                return super().create(validated_data)
            raise serializers.ValidationError("Invalid ID Provided")
        raise serializers.ValidationError("You don't have the permission")


class DesignDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Design

        fields = [
            "id",
            "slug",
            "creator",
            "title",
            "synopsis",
            "illustration",
            "tags",
            "release_date",
            "likes",
            "typeof",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        req_user = request.user

        if req_user.is_creator:
            try:
                req_creator = CreatorProfile.objects.get(creator=req_user)
            except CreatorProfile.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
            if req_creator == instance.creator:
                if validated_data.get("illustration"):
                    extension = validated_data.get("illustration").name.split(".")[-1]
                    if validated_data.get("title"):
                        title = validated_data.get("title")
                        generated_name = f"{title}.{extension}"
                        validated_data.get("illustration").name = generated_name
                        print(validated_data.get("illustration").name)
                return super().update(instance, validated_data)
            raise serializers.ValidationError(
                "You do not have the required permission."
            )
        raise serializers.ValidationError("You do not have the required permission.")


class VideoCreateSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Video
        fields = [
            "id",
            "slug",
            "creator",
            "title",
            "thumbnail",
            "synopsis",
            "video_file",
            "tags",
            "likes",
            "typeof",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        req_user = request.user

        if req_user.is_creator:
            try:
                creator_prof = CreatorProfile.objects.get(creator=req_user)
            except CreatorProfile.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
            if validated_data.get("creator") == creator_prof:
                if validated_data.get("thumbnail"):
                    title = validated_data.get("title")
                    thumbnail_extension = validated_data.get("thumbnail").name.split(
                        "."
                    )[-1]
                    generated_name = f"{title}.{thumbnail_extension}"
                    validated_data.get("thumbnail").name = generated_name
                if validated_data.get("video_file"):
                    title = validated_data.get("title")
                    video_extension = validated_data.get("video_file").name.split(".")[
                        -1
                    ]
                    generated_name = f"singles_{title}.{video_extension}"
                    validated_data.get("video_file").name = generated_name
                return super().create(validated_data)
            raise serializers.ValidationError("Invalid ID Provided")
        raise serializers.ValidationError(
            "You do not have the permission to perform this action"
        )


class VideoDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    likes = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="creatorprofile-detail"
    )

    class Meta:
        model = Video
        fields = [
            "id",
            "slug",
            "title",
            "synopsis",
            "thumbnail",
            "video_file",
            "tags",
            "release_date",
            "creator",
            "likes",
            "typeof",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        req_user = request.user
        if req_user.is_creator:
            try:
                creator_profile = CreatorProfile.objects.get(creator=req_user)
            except CreatorProfile.DoesNotExist:
                raise serializers.ValidationError("User does not exist")

            if creator_profile == instance.creator:
                if validated_data.get("thumbnail"):
                    if validated_data.get("title"):
                        title = validated_data.get("title")
                        extension = validated_data.get("thumbnail").name.split(".")[-1]
                        generated_file_name = f"{title}.{extension}"
                        validated_data.get("thumbnail").name = generated_file_name
                return super().update(instance, validated_data)

            raise serializers.ValidationError(
                "You do not have the permission to perform this action."
            )
        raise serializers.ValidationError(
            "You do not have the permission to perform this action."
        )
