from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user, set_file_size


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
    invoice = models.ForeignKey(
        to='contractors.Invoice',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Счет',
        blank=True,
        null=True,
    )
    worklist = models.TextField(verbose_name='Требуемые работы', default='', blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    completed_at = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
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
        super(ComponentRepair, self).save(*args, **kwargs)

    def __str__(self):
        return f'Ремонт №{self.pk} компонента №{self.component.number}'


def component_repair_attachment_upload_path(instance, filename):
    return f'repairs/{instance.repair.pk}/{filename}'


class ComponentRepairAttachment(models.Model):
    """Файлы вложений для ремонтов компонентов (фото, видео и др.)"""
    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=component_repair_attachment_upload_path,
    )
    repair = models.ForeignKey(
        to='components.ComponentRepair',
        related_name='attachments',
        verbose_name='Ремонт',
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=30,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authored_component_repair_attachments',
        )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение ремонта компонента'
        verbose_name_plural = 'Вложения ремонтов компонентов'

    def save(self, *args, **kwargs):
        user = get_user()
        if not self.pk:
            self.author = user
        set_file_size(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вложение ремонта компонента {self.repair.pk}'
