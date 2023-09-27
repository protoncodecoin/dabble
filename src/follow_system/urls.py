from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContactAPIView.as_view(), name="follow"),
    path("<int:pk>/", views.ContactDetailAPIView.as_view(), name="follow-detail"),
]
