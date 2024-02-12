from django.db import models
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from taggit.managers import TaggableManager

from users_api.models import CreatorProfile


# Create your models here.
class Series(models.Model):
    """Database Model for Series"""

    creator = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="series_created",
        verbose_name="creator",
    )
    series_name = models.CharField(max_length=200, unique=True)
    series_poster = models.ImageField(
        upload_to="series/posters/%Y/%m/",
        default="default/series.jpg",
    )
    synopsis = models.TextField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="series_like", blank=True
    )
    tags = TaggableManager()

    def __str__(self):
        return self.series_name

    class Meta:
        """Meta class for Series Model"""

        verbose_name_plural = "Series"
        ordering = ["-start_date"]


class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="season")
    season_number = models.IntegerField()
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.series.series_name} season {self.season_number}"

    class Meta:
        verbose_name_plural = "Season"
        ordering = ["-release_date"]


class Base(models.Model):
    """Database Model for Series"""

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.IntegerField(
        null=False, validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    episode_title = models.CharField(max_length=500)
    description = models.TextField(max_length=700, blank=True, null=True)
    episode_release_date = models.DateField(auto_now_add=True)
    publish = models.BooleanField(default=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="%(class)s_like", blank=True
    )
    tags = TaggableManager()

    # views

    class Meta:
        """Meta class to set this model as an abstract class"""

        abstract = True
        ordering = ["-episode_release_date"]

    def __str__(self):
        return f"{self.series.series_name}, Episode: {self.episode_number}"


class Story(Base):
    """Database Model for Story"""

    thumbnail = models.ImageField(
        upload_to="stories/thumbnails/%Y/%m/", default="default/story.jfif", blank=True
    )
    content = models.TextField(blank=False)

    class Meta:
        """Meta class for Story Model"""

        verbose_name = "Story"
        verbose_name_plural = "Stories"


class Anime(Base):
    """Database Model for Series"""

    anime_thumbnail = models.ImageField(
        upload_to="animations/thumbnails/%Y/%m/",
        default="default/anime.jfif",
        blank=True,
    )
    video_file = models.FileField(upload_to="animations/video/%Y/%m/", blank=False)

    class Meta:
        """Meta class for Anime Model"""

        verbose_name = "Animation"
        verbose_name_plural = "Animations"


class Media(models.Model):
    """Model for single Movies/Animations"""

    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name="singles"
    )
    title = models.CharField(max_length=150)
    synopsis = models.CharField(max_length=300)
    release_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(
        upload_to="singles/poster/%Y/%m/", default="default/singles.jfif", blank=True
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "text",
                "video",
            )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    class Meta:
        """Meta class for Single Model."""

        verbose_name = "Media"
        verbose_name_plural = "Media"

    def __str__(self):
        return self.title


class Text(models.Model):
    """Model for single story content"""

    content = models.TextField()


class Video(models.Model):
    """Model for single video content"""

    video_file = models.FileField(upload_to="singles/video/%Y/%m/", blank=False)
