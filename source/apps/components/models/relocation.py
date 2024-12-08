from django.db import models

from apps.common.models import Relocation


class ComponentRelocation(Relocation):
    """Перемещение компонентов"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='relocations',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )

    class Meta:
        verbose_name = 'Перемещение компонента'
        verbose_name_plural = 'Перемещения компонентов'
        ordering = ['-date']

    def __str__(self):
        return self.component.number + ' в ' + self.to_site.name + ' ' + self.date.strftime("%d-%m-%Y")
