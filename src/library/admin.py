from django.contrib import admin
from .models import Book

# Register your models here.


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    """Register Book Model to Admin Site"""

    list_display = [
        "title",
        "added_on",
        "book_category",
        "added_by",
        "chapters",
        "pages",
    ]
    list_filter = [
        "added_on",
        "updated_on",
        "book_category",
        "chapters",
        "pages",
    ]
    search_fields = ["title", "description"]
