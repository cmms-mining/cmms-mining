from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.common.services import set_file_size
from apps.equip_documents.models import EquipmentDocument


@receiver(pre_save, sender=EquipmentDocument)
def set_file_size_equip_document(sender, instance, **kwargs):
    set_file_size(instance)
