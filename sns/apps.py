from django.apps import AppConfig


class SnsConfig(AppConfig):
    name = 'sns'

    def ready(self) :
        import sns.signals.handlers