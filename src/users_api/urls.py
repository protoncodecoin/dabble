from django.urls import path

from . import views

app_name = "users"

urlpatterns = [

    path("favorites/", views.FavoriteAPIView.as_view()),
    # path("profile-search", views.search_creators, name="search_creators"),
    path("creators-profile/", views.CreatorListAPIView.as_view()),
    path("creator/", views.CreatorDetailAPIView.as_view()),
    path("users-profile/", views.UsersProfileListAPIView.as_view()),
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
