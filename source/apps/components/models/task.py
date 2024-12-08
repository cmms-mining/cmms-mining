from django.db import models

from apps.tasks.models import Task


class ComponentTask(Task):
    """Задания для компонента"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
        )

    class Meta:
        verbose_name = 'Задача компонента'
        verbose_name_plural = 'Задачи компонентов'
