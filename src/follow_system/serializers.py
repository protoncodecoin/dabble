from rest_framework import serializers

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "user_from",
            "user_to",
        ]


class FollowDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "user_from",
            "user_to",
            "created",
        ]
