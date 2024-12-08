from django.apps import AppConfig


class EquipmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.equipments"

    def ready(self):
        import apps.equipments.signals
