from django.db import models


class ComponentRepair(models.Model):
    """Ремонты компонентов"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )
    worklist = models.TextField(verbose_name='Требуемые работы', default='')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    completed_at = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
    completed = models.BooleanField(verbose_name='Выполнено', default=False)

    class Meta:
        verbose_name = 'Ремонт компонента'
        verbose_name_plural = 'Ремонты компонентов'
        ordering = ['-pk']

    def __str__(self):
        return self.component.number + ' ' + self.created_at.strftime("%d-%m-%Y")
