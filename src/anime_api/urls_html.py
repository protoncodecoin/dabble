from django.urls import path

from anime_api import views_html

app_name = "anime_html"

urlpatterns = [
    path("", views_html.index, name="index"),
    path("dashboard/", views_html.dashboard, name="dashbaord"),
    path("search/", views_html.search, name="search"),
    path("virtualtour/", views_html.virtualtour, name="virtualtour"),
    path(
        "count/<content_type>/<int:id>/",
        views_html.detail_post_count,
        name="post_detail",
    ),
    path(
        "<int:id>/<slug:slug>/",
        views_html.profile,
        name="profile_page",
    ),
    path("viewed/most_viewed/", views_html.post_ranking, name="most_viewed"),
    path("gallery/", views_html.gallery, name="gallery"),
    path("gallery/animation/", views_html.gallery_animation, name="gallery_animation"),
    path("gallery/film/", views_html.gallery_film, name="gallery_film"),
    path(
        "gallery/illustrations/",
        views_html.gallery_illustration,
        name="gallery_illustration",
    ),
    path(
        "gallery/writte-stories/",
        views_html.gallery_stories,
        name="gallery_stories",
    ),
    path(
        "gallery/photography/",
        views_html.photography,
        name="gallery_photography",
    ),
]
