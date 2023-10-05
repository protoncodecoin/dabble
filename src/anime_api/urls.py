from django.urls import path


from . import views

urlpatterns = [
    path(
        "likes/<str:content_type>/<str:content_id>/",
        views.like_and_unlike,
        name="like_and_unlike",
    ),
    path(
        "comments/<str:content_type>/<int:content_id>", views.comments, name="comments"
    ),
    path("series/", views.SeriesListAPI.as_view(), name="series-list"),
    path("series/create/", views.SeriesCreateAPI.as_view()),
    path("series/<int:pk>/", views.SeriesDetailAPI.as_view(), name="series-detail"),
    # series url path
    path("stories/", views.StoryAPI.as_view(), name="stories-list"),
    path("stories/<int:pk>/", views.StoryDetailAPI.as_view(), name="story-detail"),
    # anime url path
    path("animes/", views.AnimeAPI.as_view(), name="animes"),
    path("animes/<int:pk>", views.AnimeDetailAPI.as_view(), name="anime-detail"),
]
