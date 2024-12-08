from django.apps import AppConfig


class BucketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.buckets'

    def ready(self):
        import apps.buckets.signals
