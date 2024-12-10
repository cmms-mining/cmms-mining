from django.apps import AppConfig


class ComponentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.components'

    def ready(self):
        import apps.components.signals