from django.contrib import admin

from .models import Comment

# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "date_posted",
        "id",
        "is_approved",
        "parent",
        "text",
    ]

    list_filter = [
        "date_posted",
        "is_approved",
    ]
    search_fields = ["comment"]
