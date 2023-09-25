from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="comment-detail", lookup_field="pk"
    )

    class Meta:
        model = Comment
        fields = [
            "url",
            "id",
            "user",
            "target_id",  # id of what you are comment on. Series, Anime, story
            "comment",
            # "target_ct",
            # "created",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "comment",
            "created",
            "target_id",
            "target_ct",
        ]
