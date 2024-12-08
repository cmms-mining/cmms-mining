from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.common.services import get_user

if TYPE_CHECKING:
    from . import Bucket


class BucketTechState(models.Model):
    """Техсостояние ковшей"""
    bucket = models.ForeignKey(
        to='buckets.Bucket',
        related_name='techstates',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
    )
    date = models.DateField(verbose_name='Дата техсостояния')
    techstate = models.ForeignKey(
        to='common.TechStateOption',
        related_name='buckets_techstates',
        on_delete=models.CASCADE,
        verbose_name='Техсостояние',
    )
    is_operable = models.BooleanField(verbose_name='Подлежит эксплуатации', default=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Техсостояние ковша'
        verbose_name_plural = 'Техсостояния ковшей'
        ordering = ['-date']

    def __str__(self):
        return self.bucket.number + ' ' + self.techstate.name + ' ' + self.date.strftime("%d-%m-%Y")

    def is_edit_allowed(self) -> bool:
        """Доступность к редактированию (только последнее техсостояние и в день создания)"""
        bucket: Bucket = self.bucket
        if int(self.pk) == int(BucketTechState.objects.filter(bucket=bucket).first().pk) and \
                self.created_at.date() == timezone.localtime().date() and self.author == get_user():
            return True
