from django.db import models
from django.utils import timezone

from apps.common.models import Deinstallation, Installation
from apps.common.services import get_user


class BucketInstallation(Installation):
    """Установки ковшей"""
    bucket = models.ForeignKey(
        to='buckets.Bucket',
        related_name='bucket_installations',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
    )

    class Meta:
        verbose_name = 'Установка ковша'
        verbose_name_plural = 'Установки ковшей'
        ordering = ['-date']

    def __str__(self):
        return self.bucket.number + ' на ' + self.to_equipment.number

    def is_edit_allowed(self) -> bool:
        """Доступность к редактированию (только последняя установка и в день создания)"""
        bucket = self.bucket
        if int(self.pk) == int(BucketInstallation.objects.filter(bucket=bucket).first().pk) and \
                self.created_at.date() == timezone.localtime().date() and self.author == get_user():
            return True


class BucketDeinstallation(Deinstallation):
    """Демонтаж ковшей"""
    bucket = models.ForeignKey(
        to='buckets.Bucket',
        related_name='bucket_deinstallations',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
    )

    class Meta:
        verbose_name = 'Демонтаж ковша'
        verbose_name_plural = 'Демонтажи ковшей'
        ordering = ['-date']

    def __str__(self):
        return self.bucket.number + ' с ' + self.from_equipment.number

    def is_edit_allowed(self) -> bool:
        """Доступность к редактированию (только последний демонтаж и в день создания)"""
        bucket = self.bucket
        if int(self.pk) == int(BucketDeinstallation.objects.filter(bucket=bucket).first().pk) and \
                self.created_at.date() == timezone.localtime().date() and self.author == get_user():
            return True
