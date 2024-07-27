from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("book/create/", views.BookCreateAPIView.as_view()),
    path("books/", views.BookListAPIView.as_view()),
    path("books/<int:pk>/", views.BookDetailAPIView.as_view()),
    path(
        "books/<user_id>/favorites",
        views.FavoriteBooks.as_view(),
        name="favorite_books",
    ),
]
