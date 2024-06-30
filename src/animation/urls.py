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

from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView

from rest_framework_simplejwt import views as jwt_views

from users_api.views import MyTokenObtainPairView, MyTokenObtainPairView2

from users_api.views import (
    email_confirm_redirect,
    password_reset_confirm_redirect,
    GoogleAuthRedirect,
    GoogleRedirectURIView,
)


from dj_rest_auth.registration.views import RegisterView, ResendEmailVerificationView
from dj_rest_auth.views import LogoutView, UserDetailsView, PasswordResetView


from users_api.urls import router

urlpatterns = [
    path("admin/", admin.site.urls),
    # RENDER HTML URLS
    path("socialize/", include("chat.urls", namespace="chat")),
    path("users/m/", include("users_api.urls_html", namespace="users_html")),
    path("", include("anime_api.urls_html", namespace="anime_html")),
    path("books/", include("library.urls_html", namespace="library_html")),
    # END OF RENDER HTML URLS
    path("api/v1/auth/register/", RegisterView.as_view(), name="rest_register"),
    path(
        "api/v1/auth/register/verify-email/",
        VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    path(
        "api/v1/auth/register/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path(
        "api/v1/auth/account-confirm-email/<str:key>/",
        email_confirm_redirect,
        name="account_confirm_email",
    ),
    path(
        "api/v1/auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "api/v1/auth/password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "api/v1/auth/password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path(
        "api/v1/auth/password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "api/v1/auth/login/", MyTokenObtainPairView.as_view(), name="rest_login"
    ),  # overrides the login url provided by dj-rest-auth
    path(
        "api/v1/auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
    ),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="rest_logout"),
    # Django auth urls
    path("api/v1/api-auth/", include("rest_framework.urls")),
    # Django Rest User Detail url
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    # Google social Oauth2
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("google-signup/", GoogleAuthRedirect.as_view()),
    path("callback/google", GoogleRedirectURIView.as_view(), name="google_redirect"),
    # API URLS
    path("content/", include("anime_api.urls", namespace="animes")),
    path("comment/", include("comment_system.urls", namespace="comment")),
    path("library/", include("library.urls", namespace="library")),
    # USER ROUTERS
    path("", include(router.urls)),
    # USER FAVOURITE
    path("actions/", include("users_api.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
