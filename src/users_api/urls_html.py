from django.urls import path

from users_api import views_html

app_name = "users_html"

urlpatterns = [
    path("login/", views_html.user_login, name="login"),
    path("signup/", views_html.signup, name="signup"),
    path("logout/", views_html.user_logout, name="logout"),
    path("activation/<uidb64>/<token>/", views_html.activate, name="activate"),
]
