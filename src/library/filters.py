import django_filters
from .models import Book


class BooksFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ["book_category"]
