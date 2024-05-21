from django.apps import AppConfig


class AnimeApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "anime_api"

    def ready(self) -> None:
        from django.db.models.signals import m2m_changed
        from .signals import (
            series_m2m_add_remove_like,
            written_story_m2m_add_remove_like,
            text_content_m2m_add_remove_like,
            video_content_m2m_add_remove_like,
            design_content_m2m_add_remove_like,
        )
        from .models import Series, WrittenStory, Text, Video, Design

        m2m_changed.connect(series_m2m_add_remove_like, sender=Series.likes.through)

        m2m_changed.connect(
            written_story_m2m_add_remove_like, sender=WrittenStory.likes.through
        )
        m2m_changed.connect(text_content_m2m_add_remove_like, sender=Text.likes.through)

        m2m_changed.connect(
            video_content_m2m_add_remove_like, sender=Video.likes.through
        )

        m2m_changed.connect(
            design_content_m2m_add_remove_like, sender=Design.likes.through
        )
