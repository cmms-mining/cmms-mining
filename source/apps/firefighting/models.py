from django.db import models


class FirefightingSystem(models.Model):
    equipment = models.OneToOneField(
        to='equipments.Equipment',
        related_name='firefighting',
        verbose_name='Оборудование',
        on_delete=models.CASCADE,
        )
    requires_check = models.BooleanField(verbose_name='Требует проверки', default=True)

    class Meta:
        verbose_name = 'Система пожаротушения'
        verbose_name_plural = 'Системы пожаротушения'

    def __str__(self):
        return f'Система пожаротушения {self.equipment.number}'


def attach_firefighting_check_upload_path(instance, filename):
    return f'firefighting/{instance.firefighting_system.equipment.number}' \
           f'/{instance.date.strftime("%d-%m-%Y")}/{filename}'


class FirefightingCheck(models.Model):
    firefighting_system = models.ForeignKey(
        to='firefighting.FirefightingSystem',
        related_name='firefighting_checks',
        verbose_name='Система пожаротушения',
        on_delete=models.CASCADE,
        )
    date = models.DateField(verbose_name='Дата проверки')
    attachment_file = models.FileField(upload_to=attach_firefighting_check_upload_path, verbose_name='Файл вложения')
    STATE_CHOICES = (
        ('Исправна', 'Исправна'),
        ('Неисправна', 'Неисправна'),
        ('Неустановлена', 'Неустановлена'),
    )
    state = models.CharField(
        verbose_name='Состояние',
        max_length=20,
        choices=STATE_CHOICES,
    )
    note = models.CharField(verbose_name='Примечание', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Проверка системы пожаротушения'
        verbose_name_plural = 'Проверки систем пожаротушения'

    def __str__(self):
        return f'Проверка системы пожаротушения {self.firefighting_system.equipment.number}'
