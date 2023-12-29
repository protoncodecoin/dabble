from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("all/", views.CommentAPIView.as_view(), name="all_comments"),
    path(
        "<int:pk>/",
        views.CommentDetailAPIView.as_view(),
        name="comment-detail",
    ),
]
