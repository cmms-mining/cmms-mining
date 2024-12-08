from django.contrib.auth.models import User
from django.db import models


class Installation(models.Model):
    """Установки на оборудование"""
    to_equipment = models.ForeignKey(
        to='equipments.Equipment',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Куда',
    )
    date = models.DateField(verbose_name='Дата установки')
    location = models.ForeignKey(
        to='components.ComponentInstallationLocation',
        related_name='%(class)s_installations',
        on_delete=models.CASCADE,
        verbose_name='Место установки',
        null=True,
        blank=True,
    )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['-date']


class Deinstallation(models.Model):
    """Демонтажи с оборудования"""
    from_equipment = models.ForeignKey(
        to='equipments.Equipment',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Откуда',
    )
    date = models.DateField(verbose_name='Дата демонтажа')
    reason = models.ForeignKey(
        to='common.DeinstallationReason',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Причина',
    )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['-date']


class DeinstallationReason(models.Model):
    """Причины демонтажа"""
    reason = models.CharField(verbose_name='Причина', max_length=50)

    class Meta:
        verbose_name = 'Причина демонтажа'
        verbose_name_plural = '(Справочник) Причины демонтажей'

    def __str__(self):
        return self.reason
