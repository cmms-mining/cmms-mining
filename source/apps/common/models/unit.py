from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user


class CurrentData(models.Model):
    """Хранение последних данных по юниту (местоположение, статус ремонта)"""
    location = models.ForeignKey(
        to='sites.Site',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Местоположение',
        )
    relocation_date = models.DateField(blank=True, null=True, verbose_name='Дата перемещения')
    techstate = models.ForeignKey(
        to='common.TechStateOption',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Техсостояние',
        )
    techstate_date = models.DateField(blank=True, null=True, verbose_name='Дата техсостояния')
    #  используется только в ковшах, может есть смысл перенести только в ковши?
    is_being_repaired = models.BooleanField(verbose_name='В ремонте', blank=True, null=True)
    is_operable = models.BooleanField(verbose_name='Подлежит эксплуатации', blank=True, null=True)
    updated_by = models.ForeignKey(
        verbose_name='Последний редактор',
        to=User,
        on_delete=models.CASCADE,
        null=True,
        )
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        self.updated_by = get_user()
        super().save(*args, **kwargs)
