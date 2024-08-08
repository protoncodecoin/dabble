from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("chat/", views.chat_person, name="chatty"),
    path("chat/messages/", views.MessageAPIView.as_view()),
]
