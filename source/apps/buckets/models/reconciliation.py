from django.db import models

from apps.common.models import Reconciliation


class BucketReconciliation(Reconciliation):
    """Сверки по ковшам"""
    bucket = models.ForeignKey(
        to='buckets.Bucket',
        related_name='reconciliations',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
    )

    class Meta:
        verbose_name = 'Сверка ковша'
        verbose_name_plural = 'Сверки ковшей'
        ordering = ['-date']

    def __str__(self):
        return self.bucket.number + ' ' + self.date.strftime("%d-%m-%Y")
