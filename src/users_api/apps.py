from django.apps import AppConfig


class UsersApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users_api"

    def ready(self) -> None:
        import users_api.signals
