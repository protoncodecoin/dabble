from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Anime, WrittenStory, Text, Series, Video, Design


@receiver(m2m_changed, sender=Series.likes.through)
def series_m2m_add_remove_like(sender, instance, action, pk_set, **kwargs):
    """
    signal to add or substract from total_likes when the series object is liked
    """
    if action == "post_add":
        instance.creator.total_likes += 1
        instance.creator.save()

    if action == "post_remove":
        instance.creator.total_likes -= 1
        instance.creator.save()


@receiver(m2m_changed, sender=WrittenStory.likes.through)
def written_story_m2m_add_remove_like(sender, instance, action, pk_set, **kwargs):
    """
    signal to add or substract from total_likes when the written_story object is liked
    """
    if action == "post_add":
        instance.series.creator.total_likes += 1
        instance.series.creator.save()

    if action == "post_remove":
        instance.series.creator.total_likes -= 1
        instance.series.creator.save()


@receiver(m2m_changed, sender=Anime.likes.through)
def animation_m2m_add_remove_like(sender, instance, action, pk_set, **kwargs):
    """
    signal to add or substract from total_likes when the animation object is liked
    """
    if action == "post_add":
        instance.series.creator.total_likes += 1
        instance.series.creator.save()

    if action == "post_remove":
        instance.series.creator.total_likes -= 1
        instance.series.creator.save()


@receiver(m2m_changed, sender=Text.likes.through)
def text_content_m2m_add_remove_like(sender, instance, action, pk_set, **kwargs):
    """
    signal to add or substract from total_likes when the text object is liked
    """
    if action == "post_add":
        instance.creator.total_likes += 1
        instance.creator.save()

    if action == "post_remove":
        instance.creator.total_likes -= 1
        instance.creator.save()


@receiver(m2m_changed, sender=Video.likes.through)
def video_content_m2m_add_remove_like(sender, instance, action, pk_set, **kwargs):
    """
    signal to add or substract from total_likes when the video object is liked
    """
    if action == "post_add":
        instance.creator.total_likes += 1
        instance.creator.save()

    if action == "post_remove":
        instance.creator.total_likes -= 1
        instance.creator.save()


@receiver(m2m_changed, sender=Design.likes.through)
def design_content_m2m_add_remove_like(sender, instance, action, pk_set, **kwargs):
    """
    signal to add or substract from total_likes when the design object is liked
    """
    if action == "post_add":
        instance.creator.total_likes += 1
        instance.creator.save()

    if action == "post_remove":
        instance.creator.total_likes -= 1
        instance.creator.save()
