from django.urls import path


from . import views

urlpatterns = [
    path("search", views.search_contents, name="search"),
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
    path("stories/", views.StoryListAPI.as_view(), name="stories-list"),
    path("stories/create/", views.StoryCreateAPI.as_view(), name="stories-create"),
    path("stories/<int:pk>/", views.StoryDetailAPI.as_view(), name="story-detail"),
    # anime url path
    path("animes/", views.AnimeListAPI.as_view(), name="animes-list"),
    path("anime/create/", views.AnimeCreateAPI.as_view(), name="animes-create"),
    path("animes/<int:pk>", views.AnimeDetailAPI.as_view(), name="anime-detail"),
    # seasons url path
    path("seasons/", views.SeasonListAPI.as_view()),
    path("season/create/", views.SeasonCreateAPI.as_view()),
    path("season/<int:pk>/", views.SeasonDetailAPIView.as_view()),
]
