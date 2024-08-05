from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="comments:comment-detail", lookup_field="pk"
    )
    user = serializers.HyperlinkedRelatedField(
        view_name="creatorprofile-detail", read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "url",
            "user",
            "text",
            "parent",
            "object_id",  # id of what you comment on. Series, Anime, story
            "content_type",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name="creatorprofile-detail", read_only=True
    )
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "text",
            "parent",
            "date_posted",
            "replies",
            "object_id",
            "content_type",
        ]

    def get_replies(self, obj: Comment):
        if obj.is_parent:
            comments = obj.children
            serializer = CommentSerializer(
                comments, many=True, context={"request": self.context.get("request")}
            )
            return serializer.data
