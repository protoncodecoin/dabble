from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("create/", views.CommentAPIView.as_view(), name="all_comments"),
    path(
        "all/",
        views.CommentListAPIView.as_view(),
        name="comment-detail",
    ),
]
