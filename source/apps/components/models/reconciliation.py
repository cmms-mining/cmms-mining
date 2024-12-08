from django.db import models

from apps.common.models import Reconciliation


class ComponentReconciliation(Reconciliation):
    component = models.ForeignKey(
        to='components.Component',
        related_name='reconciliations',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )

    class Meta:
        verbose_name = 'Сверка компонента'
        verbose_name_plural = 'Сверки компонентов'
        ordering = ['-date']

    def __str__(self):
        return self.component.number + ' ' + self.date.strftime("%d-%m-%Y")
