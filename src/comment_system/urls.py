from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.CommentAPIView.as_view(), name="all_comments"),
]
