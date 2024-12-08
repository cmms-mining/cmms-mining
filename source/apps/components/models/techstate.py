from django.db import models

from apps.common.models import TechState


class ComponentTechState(TechState):
    """Техсостояния компонентов"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='techstates',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )

    class Meta:
        verbose_name = 'Техсостояние компонента'
        verbose_name_plural = 'Техсостояния компонентов'
        ordering = ['-date']

    def __str__(self):
        return self.component.number + ' ' + self.techstate.name + ' ' + self.date.strftime("%d-%m-%Y")
