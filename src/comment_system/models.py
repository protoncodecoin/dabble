from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE
    )
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username} made a comment on {self.target_ct}"
