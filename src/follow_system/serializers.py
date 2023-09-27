from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "user_from",
            "user_to",
        ]


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "user_from",
            "user_to",
            "created",
        ]
