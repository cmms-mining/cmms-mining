from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    Bucket, BucketCurrentData, BucketDeinstallation, BucketInstallation, BucketRelocation, BucketRepair, BucketTechState,
)


@receiver(post_save, sender=BucketRelocation)
@receiver(post_save, sender=BucketInstallation)
@receiver(post_save, sender=BucketDeinstallation)
@receiver(post_save, sender=BucketTechState)
@receiver(post_save, sender=BucketRepair)
@receiver(post_delete, sender=BucketRelocation)
@receiver(post_delete, sender=BucketInstallation)
@receiver(post_delete, sender=BucketDeinstallation)
@receiver(post_delete, sender=BucketTechState)
@receiver(post_delete, sender=BucketRepair)
def update_bucket_current_data(sender, instance, **kwargs):
    current_data, created = BucketCurrentData.objects.get_or_create(
        bucket=instance.bucket,
    )
    bucket: Bucket = instance.bucket
    if bucket.get_relocation():
        current_data.location = bucket.get_location()
        current_data.relocation_date = bucket.get_relocation().date
    current_data.equipment = bucket.get_equipment()
    if bucket.get_techstate():
        current_data.techstate = bucket.get_techstate().techstate
        current_data.techstate_date = bucket.get_techstate().date
    current_data.is_operable = bucket.get_is_operable()
    current_data.is_being_repaired = bucket.get_is_being_repaired()
    current_data.save()
