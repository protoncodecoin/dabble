from .models import GroupMessage, Message
from rest_framework import serializers

from users_api.serializers import RCreatorSerializer, RCustomUserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sent_on_formatted = serializers.SerializerMethodField()
    from_user = RCustomUserSerializer()
    to_who = RCustomUserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_sent_on_formatted(self, obj: Message):
        return obj.sent_on.strftime("%d-%m-%Y %H:%M:%S")
