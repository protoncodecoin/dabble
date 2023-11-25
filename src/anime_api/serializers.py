from rest_framework import serializers

from .models import Series, Story, Anime

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
    # slug = serializers.SerializerMethodField()
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
        ]

        extra_kwargs = {
            "slug": {"write_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user.creator_profile
        series_name = self.validated_data["series_name"]
        series_poster = self.validated_data["series_poster"]
        synopsis = self.validated_data["synopsis"]

        return Series.objects.create(
            creator=user,
            series_name=series_name,
            synopsis=synopsis,
            series_poster=series_poster,
        )

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)
        # serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)


class SeriesDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="creator", read_only=True)
    creator = serializers.ReadOnlyField(source="creator.username")
    comments = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField(source="likes.count")
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()
    # tags = serializers.ReadOnlyField(source="tags.object.all")

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

    # def get_tags(self, obj):
    #     tags = obj.tags.all()
    #     return tags


class StorySerializer(serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="story-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season_number = serializers.ReadOnlyField(source="season.season_number")

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
            "season",
            "season_number",
        ]


class StoryCreateSerializer(serializers.ModelSerializer):
    """A class serializer to serialize data from Story Model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="story-detail", lookup_field="pk"
    )
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season_number = serializers.ReadOnlyField(source="season.season_number")

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
        series_id = validated_data["series"]
        season_id = validated_data["season"]
        episode_number = validated_data["episode_number"]
        episode_title = validated_data["episode_title"]
        description = validated_data["description"]
        thumbnail = validated_data["thumbnail"]
        content = validated_data["content"]

        return Story.objects.create(
            series=series_id,
            season=season_id,
            episode_number=episode_number,
            episode_title=episode_title,
            content=content,
            description=description,
            thumbnail=thumbnail,
        )


class StoryDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator", read_only=True)
    series_name = serializers.ReadOnlyField(source="series.series_name")
    user_has_liked = serializers.SerializerMethodField()
    likes = serializers.ReadOnlyField(source="likes.count")
    comments = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()
    season_number = serializers.ReadOnlyField(source="season.season_number")

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
            "owner",
            "comments",
        ]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user.creator_profile
        creator = data["series"].creator

        if user == creator:
            if data["series"] == data["season"].series:
                return data
            raise serializers.ValidationError(
                "ID of selected series do not match with season_series"
            )
        raise serializers.ValidationError(
            "You don't have permission to modity story obj"
        )

    def update(self, instance, validated_data):
        return super().update(instance=instance, validated_data=validated_data)

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
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    season_number = serializers.ReadOnlyField(
        source="season.season_number", read_only=True
    )

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
            "thumbnail",
            "season",
            "season_number",
            "creator",
        ]


class AnimeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = [
            "pk",
            "series",
            "season",
            "episode_number",
            "episode_title",
            "description",
            "thumbnail",
            "file",
        ]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user.creator_profile
        creator = data["series"].creator

        if user == creator:
            qs = Anime.objects.filter(
                series=data["series"],
                season=data["season"],
                episode_title=data["episode_title"],
                episode_number=data["episode_number"],
            )
            if data["series"] != data["season"].series:
                raise serializers.ValidationError(
                    "id of series and season_series do not match. Please check the ids of both field or create a new season obj for the series if you haven't."
                )
            else:
                if qs.exists():
                    total_num_episodes = Anime.objects.filter(
                        series=data["series"], season=data["season"]
                    ).count()
                    data["episode_number"] += (
                        total_num_episodes if total_num_episodes else 1
                    )

                    return data
            return data
        raise serializers.ValidationError("You don't have permission to create")

    def create(self, validated_data):
        series_id = validated_data["series"]
        season_id = validated_data["season"]
        episode_title = validated_data["episode_title"]
        episode_number = validated_data["episode_number"]
        description = validated_data["description"]
        thumbnail = validated_data["thumbnail"]
        file = validated_data["file"]

        return Anime.objects.create(
            series=series_id,
            season=season_id,
            episode_title=episode_title,
            episode_number=episode_number,
            description=description,
            thumbnail=thumbnail,
            file=file,
        )


class AnimeDetailSerializer(serializers.ModelSerializer):
    owner = CreatorInlineSerializer(source="series.creator", read_only=True)
    comments = serializers.SerializerMethodField()
    series_name = serializers.ReadOnlyField(source="series.series_name")
    likes = serializers.ReadOnlyField(source="likes.count")
    user_has_liked = serializers.SerializerMethodField()
    liked_user_names = serializers.SerializerMethodField()

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
            "thumbnail",
            "likes",
            "liked_user_names",
            "file",
            "comments",
            "owner",
        ]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user.creator_profile
        creator = data["series"].creator

        if creator == user:
            if data["series"] != data["season"].series:
                raise serializers.ValidationError(
                    "ID of series and season_series do not match."
                )
            return data
        raise serializers.ValidationError("You don't have permission")

    def update(self, instance, validated_data):
        return super().update(instance=instance, validated_data=validated_data)

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

    def validate(self, data):
        request = self.context.get("request")
        creator = data["series"].creator
        user = request.user.creator_profile

        if user == creator:
            qs = Season.objects.filter(
                season_number=data["season_number"], series=data["series"]
            ).exists()
            if qs:
                raise serializers.ValidationError("Season already exist")
            return data

    def update(self, instance, validated_data):
        return super().update(instance=instance, validated_data=validated_data)


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
        creator = data["series"].creator
        user = request.user.creator_profile

        if creator == user:
            qs = Season.objects.filter(
                series=data["series"], season_number=data["season_number"]
            ).exists()
            if qs:
                raise serializers.ValidationError(
                    f"Season object with of {data['season_number']} exists"
                )
            else:
                return data
        else:
            raise serializers.ValidationError("You can edit this object")

    def create(self, validated_data):
        series_id = validated_data["series"]
        season_number = validated_data["season_number"]
        return Season.objects.create(series=series_id, season_number=season_number)
