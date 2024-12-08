from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.equip_documents.models import EquipmentDocument

from services.set_file_size import set_file_size


@receiver(pre_save, sender=EquipmentDocument)
def set_file_size_equip_document(sender, instance, **kwargs):
    set_file_size(instance)
