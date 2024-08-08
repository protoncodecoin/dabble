from django.contrib import admin

from .models import GroupMessage, Message, UserChannel

# Register your models here.


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "created_at",
        "is_appropriate",
        "sent_on",
    ]
    list_filter = [
        "is_appropriate",
        "created_at",
        "user",
        "sent_on",
    ]
    search_fields = ["text"]


@admin.register(Message)
class MessagAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "from_user",
        "to_who",
        "sent_on",
        "has_been_seen",
    ]

    list_filter = [
        "has_been_seen",
        "sent_on",
    ]
    search_fields = ["message"]


@admin.register(UserChannel)
class UserChannelsAdmin(admin.ModelAdmin):
    list_display = ["user"]
