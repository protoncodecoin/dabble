from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("favorites/all/", views.FavoritedAPIView2.as_view()),
    # path("profile-search", views.search_creators, name="search_creators"),
    path("creators-profile/all/", views.CreatorListAPIView.as_view()),
    path(
        "creator/<int:pk>/", views.CreatorDetailAPIView.as_view(), name="creator-detail"
    ),
    path(
        "creators/<int:creator_pk>/followers/", views.CreatorFollowersAPIView.as_view()
    ),
    path("users-profile/all/", views.UsersProfileListAPIView.as_view()),
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
]
