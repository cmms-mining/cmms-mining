from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from services.set_file_size import set_file_size

from .models import Equipment, EquipmentCurrentData, EquipmentRelocation, Nameplate


@receiver(pre_save, sender=Nameplate)
def set_file_size_nameplate(sender, instance, **kwargs):
    set_file_size(instance)


@receiver(post_save, sender=EquipmentRelocation)
def update_equipment_current_data(sender, instance, **kwargs):
    current_data, created = EquipmentCurrentData.objects.get_or_create(
        equipment=instance.equipment,
    )
    equipment: Equipment = instance.equipment
    current_data.location = equipment.get_location()
    current_data.save()
