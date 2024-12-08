from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import Relocation
from apps.common.services import get_user

from services.set_file_size import set_file_size


class EquipmentRelocation(Relocation):
    """Перемещение оборудования"""
    equipment = models.ForeignKey(
        to='equipments.Equipment',
        related_name='relocations',
        on_delete=models.CASCADE,
        verbose_name='Оборудование',
    )
    order = models.ForeignKey(
        to='equipments.RelocationOrder',
        related_name='equipments_relocations',
        on_delete=models.CASCADE,
        verbose_name='Приказ',
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['equipment', 'order'], name='unique_equipment_order')]
        verbose_name = 'Перемещение оборудования'
        verbose_name_plural = 'Перемещения оборудования'
        ordering = ['-date']

    def __str__(self):
        return f'Перемещение {self.pk}'


def validate_scan_file(value):
    if not value.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
        raise ValidationError('Допустимы только файлы PDF, JPG или PNG.')


def order_scan_upload_path(instance, filename):
    return f'orders/scan/{instance.date.strftime("%Y%m%d")}-{instance.number}/{filename}'


class RelocationOrder(models.Model):
    """Приказы на перемещение оборудования"""
    number = models.CharField(verbose_name='Номер приказа', max_length=20)
    date = models.DateField(verbose_name='Дата приказа')
    from_site = models.ForeignKey(
        to='sites.Site',
        related_name='orders_from_site',
        on_delete=models.CASCADE,
        verbose_name='Откуда',
    )
    to_site = models.ForeignKey(
        to='sites.Site',
        related_name='orders_to_site',
        on_delete=models.CASCADE,
        verbose_name='Куда',
    )
    scan = models.FileField(
        verbose_name='Скан приказа',
        upload_to=order_scan_upload_path,
        blank=True,
        null=True,
        validators=[validate_scan_file],
    )
    equipments = models.ManyToManyField(
        to='equipments.Equipment',
        related_name='orders',
        verbose_name='Оборудование',
        blank=True,
    )
    STATUS_CHOICES = (
        ('waiting', 'В ожидании актов'),
        ('completed', 'Выполнен'),
        ('invalid', 'Отменен'),
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='authored_orders')
    updated_by = models.ForeignKey(
        verbose_name='Последний редактор',
        to=User,
        on_delete=models.CASCADE,
        related_name='orders_last_edited',
        null=True,
        )
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['number', 'date'], name='unique_number_date')]
        verbose_name = 'Приказ на перемещение оборудования'
        verbose_name_plural = 'Приказы на перемещения оборудования'
        ordering = ['-date']

    def save(self, *args, **kwargs):
        user = get_user()
        if not self.pk:
            self.author = user
        self.updated_by = user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number + ' от ' + self.date.strftime('%d-%m-%Y')


def relocation_attachment_upload_path(instance, filename):
    return f'equipment_relocations/{instance.equipment_relocation.equipment.number}' \
           f'/{instance.equipment_relocation.pk}/{filename}'


class RelocationAttachment(models.Model):
    """Файлы вложений для перемещений оборудования (акты прием-передачи)"""
    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=relocation_attachment_upload_path,
        validators=[validate_scan_file],
    )
    equipment_relocation = models.ForeignKey(
        to='equipments.EquipmentRelocation',
        related_name='attachments',
        verbose_name='Перемещение',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authored_relocation_attachments',
        )
    updated_by = models.ForeignKey(
        verbose_name='Последний редактор',
        to=User,
        on_delete=models.CASCADE,
        related_name='relocation_attachments_last_edited',
        )
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True, null=True)
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение перемещения оборудования'
        verbose_name_plural = 'Вложения перемещений оборудования'

    def save(self, *args, **kwargs):
        user = get_user()
        if not self.pk:
            self.author = user
        self.updated_by = user
        set_file_size(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вложение к перемещению {self.equipment_relocation.pk}'
