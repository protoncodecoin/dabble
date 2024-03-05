from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

from users_api.models import UserProfile


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
        UserProfile, related_name="comments", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)  # id of series
    content_object = GenericForeignKey("content_type", "object_id")  # object created
    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username} made a comment on {self.content_type}"
