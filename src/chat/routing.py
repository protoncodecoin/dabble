from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r"ptp/chat/<str:name>/", consumers.chatConsumer.as_asgi()),
]
