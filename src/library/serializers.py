from rest_framework import serializers

from .models import Book

from users_api.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    """Serializer class to serialize books"""

    uploader = serializers.ReadOnlyField(source="added_by.creator.username")

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "cover",
            "slug",
            # "added_by",
            "book_description",
            "book_category",
            "book",
            "chapters",
            "pages",
            "author",
            "uploader",
            "added_by",
            "external_link",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        req_user = request.user

        if req_user.is_creator and req_user.is_superuser:
            if validated_data.get("added_by"):
                admin = validated_data.get("added_by").creator.email
                try:
                    admin_creator_prof = CustomUser.objects.get(email=admin)
                    pass
                except CustomUser.DoesNotExist:
                    raise serializers.ValidationError("Permission not allowed")
                if admin_creator_prof.is_superuser:
                    print("user is found", validated_data.get("added_by"))
                    return super().create(validated_data)
                raise serializers.ValidationError("User is not an admin")
            raise serializers.ValidationError("User ID not provided")
        raise serializers.ValidationError("User is not a creator or admin")


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Detail of Book
    """

    posted_by = serializers.ReadOnlyField(source="added_by.creator.email")

    class Meta:
        model = Book
        fields = [
            "id",
            "added_by",
            "posted_by",
            "title",
            "slug",
            "cover",
            "book_description",
            "book_category",
            "chapters",
            "pages",
            "author",
            "added_on",
            "updated_on",
            "book",
            "external_link",
        ]
        read_only_fields = ["added_on", "updated_on"]

        # def update(self, instance, validated_data):
        #     request = self.context.get("request")

        #     if request.user.is_creator and request.user.is_superuser:
        #         print("True")

        #         return super().update(instance, validated_data)
