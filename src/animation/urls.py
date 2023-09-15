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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from anime_api.urls import urlpatterns as anime_api_url
from users_api.urls import urlpatterns as users_api_url

api_url_patterns = [
    path("content/", include(anime_api_url)),
    path("users/", include(users_api_url)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(api_url_patterns),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
