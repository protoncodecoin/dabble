from rest_framework import serializers

from users_api.serializers import UserProfileSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="comments:comment-detail", lookup_field="pk"
    )
    user = serializers.HyperlinkedRelatedField(
        view_name="users:commonuser-detail", read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "url",
            "user",
            "object_id",  # id of what you comment on. Series, Anime, story
            "text",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    post_url = serializers.HyperlinkedRelatedField(
        view_name="animes:sveries-detail", lookup_field="pk", read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "text",
            "post_url",
            "object_id",
            "content_type",
            "created",
        ]
