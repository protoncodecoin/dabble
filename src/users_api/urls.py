from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("favorites/all/", views.FavoritedAPIView2.as_view()),
    # path("profile-search", views.search_creators, name="search_creators"),
    path("creators-profile/", views.CreatorListAPIView.as_view()),
    path(
        "creator/<int:pk>/", views.CreatorDetailAPIView.as_view(), name="creator-detail"
    ),
    path("users-profile/", views.UsersProfileListAPIView.as_view()),
    path(
        "commonuser/<int:pk>/",
        views.UserProfileDetailAPIView.as_view(),
        name="commonuser-detail",
    ),
    path("all-users/", views.AllUsersListAPIView.as_view()),
    path(
        "follow/<int:creator_id>/",
        views.follow_and_unfollow,
        name="follow_and_unfollow",
    ),
    path(
        "favorites/<str:content_type>/<int:content_id>/",
        views.add_remove_favorite,
        name="add_remove_fav",
    ),
]
