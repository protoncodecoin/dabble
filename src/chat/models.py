from django.db import models
from users_api.models import CreatorProfile
from django.conf import settings


class GroupMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_appropriate = models.BooleanField(default=True)
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} sent a message on {self.sent_on}"


class Message(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_msg"
    )
    to_who = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_who"
    )
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    has_been_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} sent a message to {self.to_who}"

    class Meta:
        ordering = ["sent_on"]


class UserChannel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_channel"
    )
    channel_name = models.TextField()
