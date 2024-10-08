from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify
from taggit.managers import TaggableManager

from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Extends the AbstractUser Model of Django to Customize the User model"""

    # username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    is_creator = models.BooleanField(
        default=False,
        help_text="Specify whether user is creator or not. Default is set to False",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CreatorProfile(models.Model):
    """Profile for Creators on the site"""

    creator = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="creator_profile",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(blank=True, max_length=200)
    background_image = models.ImageField(
        upload_to="creatorProfile/I%Y/%m/%d", blank=True, default="default/default.jpg"
    )
    programme = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    biography = models.CharField(max_length=500, blank=True, null=True)
    creator_logo = models.ImageField(
        upload_to="creatorProfile/%Y/%m/%d/",
        blank=True,
        default="default/default.jpg",
    )
    following = models.ManyToManyField(
        "self", through="Follow", symmetrical=False, related_name="followers"
    )
    total_likes = models.IntegerField(default=0)
    interests = TaggableManager()
    favorite_quote = models.TextField(max_length=200, blank=True)

    def __str__(self):
        """Readable representation of the User Profile model"""
        return f"Profile of {self.creator.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.creator.username)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class to set the User Profile plural title on the site"""

        indexes = [
            models.Index(fields=["total_likes"]),
        ]
        verbose_name_plural = "Creators Profile"


class UserProfile(models.Model):
    """Profile for 3rd level users on the site"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile"
    )
    profile_img = models.ImageField(
        upload_to="userProfile/%Y/%m/%d/",
        blank=True,
        default="default/user_default.jpg",
    )
    # follows = models.ManyToManyField(
    #     CreatorProfile, through="Follow", related_name="followers", blank=True
    # )

    def __str__(self):
        """Human readable representation of the User Profile model"""
        return f"Profile of {self.user.email}"

    class Meta:
        """Meta class to set the User Profile plural title on the site"""

        verbose_name_plural = "Users Profile"


class Follow(models.Model):
    user_from = models.ForeignKey(
        CreatorProfile,
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
