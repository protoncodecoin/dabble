from django.urls import path, re_path

from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ConfirmEmailView,
)
from dj_rest_auth.views import LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from . import views

app_name = "users"

urlpatterns = [
    path("favorites/", views.FavoriteAPIView.as_view()),
    path("profile-search", views.search_creators, name="search_creators"),
    path("creators-profile/", views.CreatorListAPIView.as_view()),
    path("users-profile/", views.UsersListAPIView.as_view()),
    path("all/", views.AllUserListAPI.as_view()),
    path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    path("register/", RegisterView.as_view(), name="account_signup"),
    # path("login/", LoginView.as_view()),
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view()),
    path("verify-email", VerifyEmailView.as_view(), name="rest_verify_email"),
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
    path(
        "follow/<int:creator_id>/",
        views.follow_and_unfollow,
        name="follow_and_unfollow",
    ),
    path(
        "favorites/<str:content_type>/<int:content_id>/",
        views.add_remove_favorite,
        name="add_remove_fav",
    ),
    path(
        "dj-rest-auth/google/login/",
        views.GoogleLoginView.as_view(),
        name="google_login",
    ),
    path("~redirect/", view=views.UserRedirectView.as_view(), name="redirect"),
]
