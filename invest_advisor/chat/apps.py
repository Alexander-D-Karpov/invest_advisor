from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "invest_advisor.chat"

    def ready(self):
        import invest_advisor.chat.signals  # noqa
