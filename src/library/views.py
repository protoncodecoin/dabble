from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from users_api.models import CreatorProfile

from .pagination import CustomPagination

from .models import Book
from .serializers import BookSerializer, BookDetailSerializer
from .filters import BooksFilter

from anime_api import permissions


# Create your views here.
class BookCreateAPIView(generics.CreateAPIView):
    """View to add books to the database"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdmin]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookListAPIView(generics.ListAPIView):
    """View to add books to the database"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    page_size = 1
    filter_backends = [DjangoFilterBackend]
    filterset_class = BooksFilter

    # filterset_fields = ["book_category"]

    # def list(self, request):
    #     """List all books"""
    #     queryset = self.get_queryset()
    #     serializer = BookSerializer(queryset, many=True)
    #     page = self.paginate_queryset(serializer.data)
    #     return self.get_paginated_response(page)


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve: pk
    Update: pk
    Delete: pk
    """

    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    # permission_classes = [permissions.IsAdmin]


# class BookAPIView(views.APIView):

#     def get(self, request):
#         """Get book"""


class FavoriteBooks(generics.ListAPIView):
    """Return a list of all user favorited books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination

    def get(self, request, user_id, format=None):
        user = user_id
        try:
            user_profile = CreatorProfile.objects.get(id=user)
        except CreatorProfile.DoesNotExist:
            return Response(
                {"message": "User Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        books = Book.objects.filter(favorited_by=user_profile)
        books_serializer = BookSerializer(books, many=True)
        return Response(
            {"results": books_serializer.data},
            status=status.HTTP_200_OK,
        )
