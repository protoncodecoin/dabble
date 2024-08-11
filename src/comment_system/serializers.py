from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from anime_api.serializers import CreatorInlineSerializer

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name="comments:comment-detail", lookup_field="pk"
    # )
    # user = serializers.HyperlinkedRelatedField(
    #     view_name="creatorprofile-detail", read_only=True
    # )
    username = serializers.ReadOnlyField(source="user.creator.username")
    owner = CreatorInlineSerializer(source="user", read_only=True)
    content_type_str = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "owner",
            "username",
            "text",
            "parent",
            "object_id",  # id of what you comment on. Series, Anime, story
            "content_type_str",
        ]

    def create(self, validated_data):
        print(validated_data, "this is the validated data")
        # Extract content_type as string and object_id from validated data
        content_type_str = validated_data.pop("content_type_str")
        object_id = validated_data.get("object_id")

        # Fetch the ContentType object based on the provided model name
        try:
            content_type = ContentType.objects.get(model=content_type_str.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type": "Invalid content type"})

        # Set the content_type in the validated data
        validated_data["content_type"] = content_type

        # Create the Comment instance
        return super().create(validated_data)


# class CommentDetailSerializer(serializers.ModelSerializer):
#     user = serializers.HyperlinkedRelatedField(
#         view_name="creatorprofile-detail", read_only=True
#     )
#     replies = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = [
#             "id",
#             "user",
#             "text",
#             "parent",
#             "date_posted",
#             "replies",
#             "object_id",
#             "content_type",
#         ]

#     def get_replies(self, obj: Comment):
#         if obj.is_parent:
#             comments = obj.children
#             serializer = CommentSerializer(
#                 comments, many=True, context={"request": self.context.get("request")}
#             )
#             return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.creator.username")
    owner = CreatorInlineSerializer(source="user", read_only=True)
    content_type_str = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        exclude = [
            "user",
            "content_type",
        ]
        # fields = [
        #     "id",
        #     "owner",
        #     "username",
        #     "text",
        #     "parent",
        #     "object_id",  # id of what you comment on. Series, Anime, story
        #     "content_type",
        # ]
