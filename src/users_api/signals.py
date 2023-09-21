from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CreatorProfile, UserProfile

User = get_user_model()


# @receiver(pre_save, sender=User)
# def create_profile(sender, instance, **kwargs):
#     """Create profile instance before user is created"""
#     if instance.is_creator:
#         if not hasattr(instance, "creatorprofile"):
#             print("Profile needs to be created 1")
#             CreatorProfile.objects.create(creator=instance)
#     else:
#         print("Something happened 2")
#         UserProfile.objects.create(user=instance)
#         pass


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     """Create profile instance after user is saved"""
#     if created:
#         print("============== This is from the post signal==========================")
#         print(dir(instance))
#         print(instance.is_creator, "it the person a creator")
#         print(instance, "this is the instance")
#         get_user = User.objects.get(email=instance)
#         print(get_user.is_creator, "This is the user from the db")
