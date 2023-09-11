from django.contrib import admin

from .models import Series, Story, Anime


# Register your models here.
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ["creator", "series_name", "start_date"]
    list_filter = ["creator", "start_date", "end_date"]
    prepopulated_fields = {"slug": ("series_name",)}
    list_display_links = ["series_name"]


@admin.register(Story)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ["episode_title", "episode_number", "episode_release_date"]
    list_filter = ["episode_release_date"]
    list_display_links = ["episode_title"]


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ["episode_title", "episode_number", "episode_release_date"]
    list_filter = ["episode_release_date"]
    list_display_links = ["episode_title"]
