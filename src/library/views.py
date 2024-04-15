from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .models import Book
from .serializers import BookSerializer, BookDetailSerializer

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

    def list(self, request):
        """List all books"""
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)


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
