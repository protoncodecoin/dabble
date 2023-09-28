from django.contrib import admin

from .models import Comment

# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "created",
        "target",
        "is_approved",
    ]

    list_filter = [
        "created",
        "is_approved",
    ]
    search_fields = ["comment"]
