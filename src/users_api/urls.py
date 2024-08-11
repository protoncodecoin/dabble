from django.urls import path
from rest_framework import routers

from . import views

app_name = "users"


router = routers.DefaultRouter()
router.register(r"userprofiles", views.CreatorViewSet, basename="creatorprofile")
router.register(r"users", views.CustomUserViewSet, basename="customuser")

urlpatterns = [
    path(
        "follow/<int:creator_id>/",
        views.follow_and_unfollow,
        name="follow_and_unfollow",
    ),
    path(
        "check_follow_status/<int:creator_id>/",
        views.check_follow_status,
        name="check_follow_status",
    ),
    path(
        "check_fav_like_status/<str:content_type>/<int:object_id>/",
        views.check_like_fav_status,
    ),
]
