from django.db import models


class ComponentRepair(models.Model):
    """Ремонты компонентов"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )
    contractor = models.ForeignKey(
        to='contractors.Contractor',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Подрядчик',
        blank=True,
        null=True,
    )
    contract = models.ForeignKey(
        to='contractors.Contract',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Договор',
        blank=True,
        null=True,
    )
    appendix = models.ForeignKey(
        to='contractors.Appendix',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Приложение к договору',
        blank=True,
        null=True,
    )
    worklist = models.TextField(verbose_name='Требуемые работы', default='', blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    completed_at = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
    completed = models.BooleanField(verbose_name='Выполнено', default=False)
    plan_end_date = models.DateField(verbose_name='Плановая дата окончания', blank=True, null=True)
    note = models.TextField(verbose_name='Примечания', blank=True, null=True)
    PRIORITY_CHOICES = (
        ('Срочно', 'Срочно'),
        ('Не срочно', 'Не срочно'),
    )
    priority = models.CharField(
        verbose_name='Приоритет',
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Не срочно',
    )

    class Meta:
        verbose_name = 'Ремонт компонента'
        verbose_name_plural = 'Ремонты компонентов'
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        if self.contract:
            self.contractor = self.contract.contractor
        elif self.appendix:
            self.contractor = self.appendix.contract.contractor
        else:
            self.contractor = None
        super(ComponentRepair, self).save(*args, **kwargs)

    def __str__(self):
        return self.component.number + ' ' + self.created_at.strftime("%d-%m-%Y")
