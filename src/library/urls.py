from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("book/create/", views.BookCreateAPIView.as_view()),
    path("books/", views.BookListAPIView.as_view()),
    path("books/<int:pk>/", views.BookDetailAPIView.as_view()),
]
