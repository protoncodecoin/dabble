from django.urls import path, re_path

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
    ConfirmEmailView,
)
from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)

# from users_api.views import email_confirm_redirect, password_reset_confirm_redirect
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from allauth.socialaccount.views import signup
from anime_api.views import GoogleLogin


from . import views

urlpatterns = [
    # path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    path("creators/", views.CreatorList.as_view()),
    path(
        "account-confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
    ),
    path("register/", RegisterView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path(
        "follow/<int:creator_id>/",
        views.follow_and_unfollow,
        name="follow_and_unfollow",
    ),
    # email verification
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("signup/", signup, name="socialaccount_signup"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
