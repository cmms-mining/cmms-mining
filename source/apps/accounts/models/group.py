from django.contrib.auth.models import Group
from django.db import models


class CustomGroup(Group):
    """Группа пользователей"""
    site = models.OneToOneField(
        to='sites.Site',
        related_name='group',
        verbose_name='Проект',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        )
    workcenter = models.OneToOneField(
        to='sites.WorkCenter',
        related_name='group',
        verbose_name='Участок',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        )

    class Meta:
        verbose_name = 'Группа пользователей'
        verbose_name_plural = 'Группы пользователей'
