from django.contrib import admin

from .models import Follow

# Register your models here.


@admin.register(Follow)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        # "user_from",
        # "user_to",
        "created",
    ]

    list_filter = [
        "created",
    ]
