from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/room/all/", consumers.GroupChatConsumer.as_asgi()),
    path("ws/chat/individual/<int:id>/", consumers.IndividualChatConsumer.as_asgi()),
]
