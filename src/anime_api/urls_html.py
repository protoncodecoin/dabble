from django.urls import path

from anime_api import views_html

app_name = "anime_html"

urlpatterns = [
    path("", views_html.index, name="index"),
    path(
        "<content_type>/<int:id>/<slug:slug>/",
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
]
