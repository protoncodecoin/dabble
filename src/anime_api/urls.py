from django.urls import path


from . import views

app_name = "animes"

urlpatterns = [
    path("search/<str:contenttype>/", views.search, name="search"),
    path(
        "action/like/<str:content_type>/<str:content_id>/",
        views.toggle_like,
        name="like_and_unlike",
    ),
    path("action/favorite/all/", views.FavoritedAPIView.as_view()),
    path(
        "action/favorite/<str:content_type>/<str:content_id>/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path(
        "actions/comment/<str:content_type>/<int:content_id>",
        views.comments,
        name="comments",
    ),
    path("series/", views.SeriesListAPI.as_view(), name="series-list"),
    path("series/create/", views.SeriesCreateAPI.as_view(), name="series-create"),
    path("series/<int:pk>/", views.SeriesDetailAPI.as_view(), name="series-detail"),
    # series url path
    path("stories/", views.StoryListAPI.as_view(), name="stories-list"),
    path("stories/create/", views.StoryCreateAPI.as_view(), name="stories-create"),
    path("stories/<int:pk>/", views.StoryDetailAPI.as_view(), name="story-detail"),
    # anime url path
    path("anime/", views.AnimeListAPI.as_view(), name="animes-list"),
    path("anime/create/", views.AnimeCreateAPI.as_view(), name="animes-create"),
    path("anime/<int:pk>/", views.AnimeDetailAPI.as_view(), name="anime-detail"),
    path("anime/top-animations/", views.AnimeListAPI.as_view()),
    # seasons url path
    path("season/", views.SeasonListAPI.as_view(), name="season-list"),
    path("season/create/", views.SeasonCreateAPI.as_view(), name="season-create"),
    path("season/<int:pk>/", views.SeasonDetailAPIView.as_view(), name="season-detail"),
    # New Media
    # Text
    path("textcontent/create/", views.TextCreateAPIView.as_view()),
    path("textcontent/", views.TextCreateAPIView.as_view()),
    path("textcontent/<int:pk>/", views.TextUpdateDeleteAPIView.as_view()),
    # Design/Illustration
    path("designcontent/", views.DesignCreateListAPIView.as_view()),
    path("designcontent/<int:pk>/", views.DesignDetailAPIView.as_view()),
    # Video
    path("videocontent/", views.VideoCreateListAPIView.as_view()),
    path("videocontent/<int:pk>/", views.VideoDetailAPIView.as_view()),
]
