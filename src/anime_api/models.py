from django.db import models
from django.utils.text import slugify

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.contrib.contenttypes.fields import GenericRelation

from taggit.managers import TaggableManager

from comment_system.models import Comment
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
    slug = models.SlugField(max_length=300, blank=True)
    series_name = models.CharField(max_length=200, unique=True)
    series_poster = models.ImageField(
        upload_to="series/posters/%Y/%m/",
        default="default/default.jpg",
    )
    synopsis = models.TextField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(
        CreatorProfile, related_name="series_like", blank=True
    )
    tags = TaggableManager()
    favorited_by = models.ManyToManyField(
        CreatorProfile, blank=True, related_name="favorite_series"
    )
    typeof = models.CharField(max_length=6, default="series")

    def __str__(self):
        return self.series_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.series_name)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for Series Model"""

        verbose_name_plural = "Series"
        ordering = ["-start_date"]


class Season(models.Model):
    OBJ_TYPE = (
        ("Anime", "Animation"),
        ("Story", "Story"),
    )
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="season")
    season_number = models.IntegerField()
    slug = models.SlugField(blank=True)
    obj_type = models.CharField(max_length=10, choices=OBJ_TYPE, default="Anime")
    release_date = models.DateTimeField(auto_now_add=True)
    typeof = models.CharField(max_length=6, default="season")

    def __str__(self):
        return f"{self.series.series_name} season {self.season_number}"

    class Meta:
        verbose_name_plural = "Season"
        ordering = ["release_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.series.series_name + "-" + str(self.season_number))
        return super().save(*args, **kwargs)


class Base(models.Model):
    """Database Model for Series"""

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="%(class)s_season"
    )
    slug = models.SlugField(max_length=300, blank=True)
    episode_number = models.IntegerField(
        null=False, validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    episode_title = models.CharField(max_length=500)
    description = models.TextField(max_length=700, blank=True, null=True)
    release_date = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=True)
    likes = models.ManyToManyField(
        CreatorProfile,
        related_name="%(class)s_like",
        blank=True,
    )
    tags = TaggableManager(blank=True)

    # views

    class Meta:
        """Meta class to set this model as an abstract class"""

        abstract = True
        # ordering = ["-episode_release_date"]

    def __str__(self):
        return f"{self.series.series_name}, Episode: {self.episode_number}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.episode_title)
        super().save(*args, **kwargs)


class WrittenStory(Base):
    """Database Model for Story"""

    thumbnail = models.ImageField(
        upload_to="stories/thumbnails/%Y/%m/", default="default/default.jpg", blank=True
    )
    content = models.TextField(blank=False)
    favorited_by = models.ManyToManyField(
        CreatorProfile, blank=True, related_name="favorite_stories"
    )
    comments = GenericRelation(Comment, related_query_name="writtenstories_comments")
    typeof = models.CharField(max_length=12, default="writtenstory")

    class Meta:
        """Meta class for Story Model"""

        verbose_name = "Written Story"
        verbose_name_plural = "Written Stories"


class Anime(Base):
    """Database Model for Series"""

    thumbnail = models.ImageField(
        upload_to="animations/thumbnails/%Y/%m/",
        default="default/anime.jfif",
        blank=True,
    )
    video_file = models.FileField(upload_to="animations/video/%Y/%m/", blank=False)
    favorited_by = models.ManyToManyField(
        CreatorProfile,
        blank=True,
        related_name="favorite_animes",
    )
    comments = GenericRelation(Comment, related_query_name="anime_comments")

    typeof = models.CharField(max_length=5, default="anime")

    class Meta:
        """Meta class for Anime Model"""

        verbose_name = "Animation"
        verbose_name_plural = "Animations"


class Text(models.Model):
    """Model for single story content"""

    creator = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    slug = models.SlugField(blank=True, max_length=300)
    title = models.CharField(
        max_length=150,
    )
    synopsis = models.TextField(max_length=300, blank=True)
    release_date = models.DateTimeField(
        auto_now_add=True,
    )
    thumbnail = models.ImageField(
        upload_to="singles/poster/%Y/%m/", default="default/default.jpg", blank=True
    )
    content = models.TextField()
    likes = models.ManyToManyField(
        CreatorProfile, related_name="liked_text", blank=True
    )
    favorited_by = models.ManyToManyField(
        CreatorProfile,
        blank=True,
        related_name="favorite_text",
    )
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment, related_query_name="text_comments")

    typeof = models.CharField(max_length=4, default="text")

    class Meta:
        verbose_name = "Text Content"
        verbose_name_plural = "Text Contents"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Video(models.Model):
    """Model for single video content"""

    creator = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    title = models.CharField(
        max_length=150,
    )
    slug = models.SlugField(blank=True, max_length=300)
    synopsis = models.TextField(max_length=300, blank=True)
    release_date = models.DateTimeField(
        auto_now_add=True,
    )
    thumbnail = models.ImageField(
        upload_to="singles/poster/%Y/%m/", default="default/default.jpg", blank=True
    )
    likes = models.ManyToManyField(
        CreatorProfile,
        related_name="liked_videos",
        blank=True,
    )
    video_file = models.FileField(
        upload_to="singles/video/%Y/%m/",
    )
    favorited_by = models.ManyToManyField(
        CreatorProfile,
        blank=True,
        related_name="favorite_video",
    )
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment, related_query_name="video_comments")

    typeof = models.CharField(max_length=5, default="video")

    class Meta:
        verbose_name = "Video Content"
        verbose_name_plural = "Video Contents"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Design(models.Model):
    """Model for Illustrations/Design"""

    creator = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    slug = models.SlugField(blank=True, max_length=300)
    title = models.CharField(
        max_length=150,
    )
    synopsis = models.TextField(max_length=300, blank=True)
    release_date = models.DateTimeField(
        auto_now_add=True,
    )
    likes = models.ManyToManyField(
        CreatorProfile, related_name="liked_illustration", blank=True
    )
    illustration = models.ImageField(
        upload_to="singles/designs/%Y/%m/",
    )
    favorited_by = models.ManyToManyField(
        CreatorProfile,
        blank=True,
        related_name="favorite_design",
    )
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment, related_query_name="design_comments")

    typeof = models.CharField(max_length=6, default="design")

    class Meta:
        verbose_name = "Design/Illustration Content"
        verbose_name_plural = "Design/Illustration Contents"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Photography(models.Model):
    creator = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    slug = models.SlugField(blank=True, max_length=300)
    title = models.CharField(
        max_length=150,
    )
    caption = models.TextField(max_length=300, blank=True)
    date_posted = models.DateTimeField(
        auto_now_add=True,
    )
    likes = models.ManyToManyField(
        CreatorProfile, related_name="liked_photography", blank=True
    )
    image = models.ImageField(
        upload_to="singles/photography/%Y/%m/",
    )
    favorited_by = models.ManyToManyField(
        CreatorProfile,
        blank=True,
        related_name="photography",
    )
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment, related_query_name="photography_comments")
    typeof = models.CharField(max_length=15, default="photography")

    class Meta:
        verbose_name = "Photography"
        verbose_name_plural = "Photography"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
