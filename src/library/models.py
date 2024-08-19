from django.db import models
from users_api.models import CreatorProfile

from django.utils.text import slugify


# Create your models here.
class Book(models.Model):
    """Model for Book"""

    CATEGORY_CHOICES = [
        ("other", "Others"),
        ("history", "History"),
        ("design-illustration", "Design/Illustration"),
        ("animation", "Animation"),
        ("videography", "Videography"),
        ("photography", "Photography"),
        ("typography", "Typography"),
        ("advertising", "Advertising"),
        ("research", "Research"),
    ]

    added_by = models.ForeignKey(CreatorProfile, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(blank=True)
    title = models.CharField(max_length=50)
    cover = models.ImageField(
        upload_to="books/covers/%Y/%m/",
        default="books/covers/default_book_image.jpeg",
        blank=True,
    )
    book_description = models.TextField(max_length=150, blank=True)
    book = models.FileField(upload_to="books/%Y/%m/")
    book_category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default="other"
    )
    pages = models.IntegerField(default=0)
    chapters = models.IntegerField(default=0)
    author = models.CharField(blank=True, max_length=200)
    added_on = models.DateTimeField(auto_now_add=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(
        CreatorProfile, related_name="favorited_books", blank=True
    )
    external_link = models.URLField(blank=True)
    typeof = models.CharField(default="book", max_length=4)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
