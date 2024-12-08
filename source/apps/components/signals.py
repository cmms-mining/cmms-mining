from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (ComponentDeinstallation, ComponentInstallation, ComponentRelocation, ComponentTechState)
from .services import update_component_current_data


@receiver(post_save, sender=ComponentRelocation)
@receiver(post_save, sender=ComponentInstallation)
@receiver(post_save, sender=ComponentDeinstallation)
@receiver(post_save, sender=ComponentTechState)
@receiver(post_delete, sender=ComponentRelocation)
@receiver(post_delete, sender=ComponentInstallation)
@receiver(post_delete, sender=ComponentDeinstallation)
@receiver(post_delete, sender=ComponentTechState)
def signal_update_component_current_data(sender, instance, **kwargs):
    component = instance.component
    update_component_current_data(component=component)
