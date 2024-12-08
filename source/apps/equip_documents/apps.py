from django.apps import AppConfig


class EquipDocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.equip_documents'

    def ready(self):
        import apps.equip_documents.signals
