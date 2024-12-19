from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.common.services import set_file_size
from apps.events.models import EventFile


@receiver(pre_save, sender=EventFile)
def set_file_size_eventfile(sender, instance, **kwargs):
    set_file_size(instance)
