import os
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Series(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="series_created",
        verbose_name="creator",
    )
    series_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    series_poster = models.ImageField(upload_to="series/posters/%Y/%m/%d/")
    synopsis = models.TextField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    # comment
    # views

    def __str__(self):
        return self.series_name

    class Meta:
        verbose_name_plural = "Series"


class EpidoseBase(models.Model):
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, related_name="%(class)s_related"
    )
    episode_number = models.IntegerField(
        null=False, validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    episode_title = models.CharField(max_length=500)
    description = models.TextField(max_length=700, blank=True)
    episode_release_date = models.DateField(auto_now_add=True)
    publish = models.BooleanField(default=True)
    # comment
    # views

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.series.series_name}, Episode: {self.episode_number}"


class Story(EpidoseBase):
    thumbnail = models.ImageField(upload_to="stories/thumbnails/%Y/%m/%d/", blank=True)
    content = models.TextField()

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"


class Anime(EpidoseBase):
    thumbnail = models.ImageField(
        upload_to="animations/thumbnails/%Y/%m/%d", blank=True
    )
    file = models.FileField(
        upload_to="animations/video/%Y/%m/%d/", verbose_name="video file"
    )

    class Meta:
        verbose_name = "Animation"
        verbose_name_plural = "Animations"
