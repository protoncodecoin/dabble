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

from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ConfirmEmailView,
)
from dj_rest_auth.views import PasswordResetConfirmView

from rest_framework_simplejwt import views as jwt_views

from users_api.views import MyTokenObtainPairView

from users_api.views import email_confirm_redirect, password_reset_confirm_redirect


from dj_rest_auth.registration.views import RegisterView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordResetView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("register/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "register/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path(
        "account-confirm-email/<str:key>/",
        email_confirm_redirect,
        name="account_confirm_email",
    ),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "login/", MyTokenObtainPairView.as_view(), name="rest_login"
    ),  # overrides the login url provided by dj-rest-auth
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
    ),
    # path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    # path(
    #     "account-confirm-email/<str:key>/",
    #     email_confirm_redirect,
    #     name="account_confirm_email",
    # ),
    # path(
    #     "password/reset/confirm/<str:uidb64>/<str:token>/",
    #     password_reset_confirm_redirect,
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "api/v1/dj-rest-auth/password/reset/confirm/<slug:uidb64>/<slug:token>/",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    # path(
    #     "api/v1/dj-rest-auth/registration/account-confirm-email/<str:key>/",
    #     ConfirmEmailView.as_view(),
    # ),
    # path(
    #     "api/v1/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")
    # ),
    # path(
    #     "api/v1/dj-rest-auth/account-confirm-email/",
    #     VerifyEmailView.as_view(),
    #     name="account_email_verification_sent",
    # ),
    path("api/v1/api-auth/", include("rest_framework.urls")),
    path("content/", include("anime_api.urls", namespace="animes")),
    path("comments/", include("comment_system.urls", namespace="comments")),
    path("users/", include("users_api.urls", namespace="users")),
    path("library/", include("library.urls", namespace="library")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
