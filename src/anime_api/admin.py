from django.contrib import admin

from .models import Series, Story, Anime, Season


# Register your models here.
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    """Registger Series Model to Admin site"""

    list_display = ["creator", "series_name", "id", "start_date"]
    list_filter = ["creator", "start_date", "end_date"]
    prepopulated_fields = {"slug": ("series_name",)}
    list_display_links = ["series_name"]


@admin.register(Story)
class StoriesAdmin(admin.ModelAdmin):
    """Registger Stories Model to Admin site"""

    list_display = [
        "season",
        "episode_title",
        "id",
        "episode_number",
        "episode_release_date",
    ]
    list_filter = ["episode_release_date"]
    list_display_links = ["episode_title"]


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    """Registger Anime Model to Admin site"""

    list_display = [
        "season",
        "episode_title",
        "id",
        "episode_number",
        "episode_release_date",
    ]
    list_filter = ["episode_release_date"]
    list_display_links = ["episode_title"]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """Register Seasom Model to Admin site"""

    list_display = ["series", "season_number", "release_date"]
    list_display_links = ["series"]
