import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from chat.models import GroupMessage, Message, UserChannel
from users_api.models import CreatorProfile, CustomUser


class GroupChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Establish connection with the client
        """
        self.user = self.scope["user"]
        self.room_group_name = "general_group_chat"

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # accept connections
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receives message sent from client
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()

        # send  message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "group_messenger",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
                # "profile_img": await self.get_profile_image(),
            },
        )
        # persist message
        await self.persist_message(message)

    # receive message from room group
    async def group_messenger(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def persist_message(self, message):
        # send message to websocket
        await GroupMessage.objects.acreate(user=self.user, text=message)


class IndividualChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope.get("user")
        self.other_person_channel = None

        # get the other user's channel the current user c is sending the message to
        self.person_id = self.scope.get("url_route").get("kwargs").get("id")

        try:
            self.to_person = await CustomUser.objects.aget(id=self.person_id)
            to_person_channel = await UserChannel.objects.aget(user=self.to_person)
            self.other_person_channel = to_person_channel.channel_name

        except (CustomUser.DoesNotExist, UserChannel.DoesNotExist):
            self.send("Invalid user id")

        try:
            user_channel = await UserChannel.objects.aget(user=self.user)
            user_channel.channel_name = self.channel_name
            await user_channel.asave()
        except UserChannel.DoesNotExist:
            await UserChannel.objects.acreate(
                user=self.user, channel_name=self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        now = timezone.now()
        text_data = json.loads(text_data)
        new_message = Message()
        new_message.from_user = self.scope.get("user")
        new_message.to_who = self.to_person
        new_message.message = text_data.get("message")
        new_message.sent_on = now
        await new_message.asave()

        data = {
            "type": "messenger",
            "data": text_data.get("message"),
            "sent_on": now.isoformat(),
            "from_user": self.scope.get("user").username,
        }

        await self.channel_layer.send(self.other_person_channel, data)

    async def messenger(self, event):
        await self.send(text_data=json.dumps(event))
