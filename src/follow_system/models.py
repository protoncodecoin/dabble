from django.db import models
from django.conf import settings

from users_api.models import CreatorProfile


# Create your models here.
class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rel_user",
        null=True,
        blank=True,
    )
    user_to = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="rel_creator",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_from} is following {self.user_to}"

    class Meta:
        verbose_name_plural = "Contacts"
