"""
URL configuration for animation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from anime_api.urls import urlpatterns as anime_api_url
from users_api.urls import urlpatterns as users_api_url
from comment_system.urls import urlpatterns as comments_url

# from follow_system.urls import urlpatterns as follow_url

from users_api.views import (
    FacebookLogin,
    GithubLogin,
    GoogleLoginView,
    UserRedirectView,
)

api_url_patterns = [
    path("content/", include(anime_api_url)),
    path("content/comments/", include(comments_url)),
    path("users/", include(users_api_url)),
    # path("follow/", include(follow_url)),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(api_url_patterns),
    ),
    path("api/v1/api-auth/", include("rest_framework.urls")),
    path("api/v1/social-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("api/v1/social-auth/github/", GithubLogin.as_view(), name="github_login"),
    path(
        "api/v1/social-auth/google/login/",
        GoogleLoginView.as_view(),
        name="google_login",
    ),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
