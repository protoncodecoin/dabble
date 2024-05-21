from django.contrib import admin

from .models import Message, Room

# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "created_at",
        "is_appropriate",
    ]
    list_filter = [
        "is_appropriate",
        "created_at",
        "user",
    ]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "host",
        "is_approved",
    ]

    list_filter = [
        "id",
        "name",
        "is_approved",
    ]
