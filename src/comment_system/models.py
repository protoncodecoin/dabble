from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from users_api.models import CreatorProfile


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
        CreatorProfile, related_name="comments", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="post_comments",
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(
        null=True, blank=True
    )  # id of what you comment on
    content_object = GenericForeignKey("content_type", "object_id")  # object created
    text = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["-date_posted"]),
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ["date_posted"]

    def __str__(self):
        return f"{self.user.creator.email} made a comment on {self.content_type}"

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
