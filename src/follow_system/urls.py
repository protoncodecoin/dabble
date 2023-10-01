from django.urls import path

from . import views

urlpatterns = [
    path("", views.FollowAPIView.as_view(), name="follow"),
    path("<int:pk>/", views.FollowDetailAPIView.as_view(), name="follow-detail"),
]
