from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.events.models import EventFile

from services.set_file_size import set_file_size


@receiver(pre_save, sender=EventFile)
def set_file_size_eventfile(sender, instance, **kwargs):
    set_file_size(instance)
