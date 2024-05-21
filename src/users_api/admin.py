from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CreatorProfile, UserProfile, Follow


class CustomUserAdmin(UserAdmin):
    """Custom fields to show on the admin site"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = (
        "username",
        "email",
        "is_active",
        "is_creator",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_creator",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "is_creator",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_creator",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    list_display_links = [
        "email",
    ]


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    """Customize the fields displayed on the admin site"""

    list_display = [
        "creator",
        "creator_logo",
        "id",
        "total_likes",
    ]
    list_display_links = [
        "id",
        "creator",
        "creator_logo",
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Customize the fields displayed on the admin site"""

    list_display = [
        "user",
        "profile_img",
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        "user_from",
        "user_to",
        "created",
    ]
    list_display_links = [
        "user_from",
        "user_to",
    ]
