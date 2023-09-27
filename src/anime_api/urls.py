from django.urls import path


from . import views

urlpatterns = [
    path("series/", views.SeriesListAPI.as_view(), name="series-list"),
    path("series/<int:pk>/", views.SeriesDetailAPI.as_view(), name="series-detail"),
    # series url path
    path("stories/", views.StoryAPI.as_view(), name="stories-list"),
    path("stories/<int:pk>/", views.StoryDetailAPI.as_view(), name="story-detail"),
    # anime url path
    path("animes/", views.AnimeAPI.as_view(), name="animes"),
    path("animes/<int:pk>", views.AnimeDetailAPI.as_view(), name="anime-detail"),
    # email
    path(
        "account-confirm-email/<str:key>/",
        views.email_confirm_redirect,
        name="account_confirm_email",
    ),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        views.password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
]
