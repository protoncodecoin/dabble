from django.db import models
from django.conf import settings

from users_api.models import CreatorProfile, UserProfile


# Create your models here.
class Follow(models.Model):
    user_from = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="creator_following",
        null=True,
        blank=True,
    )
    user_to = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name="user_followers"
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_from} is following {self.user_to}"

    class Meta:
        verbose_name_plural = "Follow"
