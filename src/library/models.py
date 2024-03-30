from django.db import models
from users_api.models import CreatorProfile


# Create your models here.
class Book(models.Model):
    """Model for Book"""

    CATEGORY_CHOICES = [
        ("OTHER", "Others"),
        ("HISTORY", "History"),
        ("DESIGN/ILLUSTRATION", "Design/Illustration"),
        ("ANIMATION/VIDEOGRAPHY", "Animation/Videography"),
    ]

    added_by = models.ForeignKey(CreatorProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    cover = models.ImageField(
        upload_to="books/covers/%Y/%m/",
        default="books/covers/default_book_image.jpeg",
        blank=True,
    )
    book_description = models.TextField(max_length=150, blank=True)
    book = models.FileField(upload_to="books/%Y/%m/")
    book_category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default="OTHER"
    )
    added_on = models.DateTimeField(auto_now_add=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return self.title
