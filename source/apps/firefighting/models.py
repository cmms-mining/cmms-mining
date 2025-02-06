from django.db import models


def attach_firefighting_check_upload_path(instance, filename):
    return f'firefighting/{instance.firefighting_system.equipment.number}' \
           f'/{instance.date.strftime("%d-%m-%Y")}/{filename}'


class FirefightingCheck(models.Model):
    """Проверки систем пожаротушения (акт проверки)"""
    firefighting_system = models.ForeignKey(
        to='firefighting.FirefightingSystem',
        related_name='firefighting_checks',
        verbose_name='Система пожаротушения',
        on_delete=models.CASCADE,
        )
    date = models.DateField(verbose_name='Дата акта проверки')
    location = models.ForeignKey(
        to='sites.Site',
        verbose_name='Место проведения проверки',
        on_delete=models.CASCADE,
        )
    attachment_file = models.FileField(
        upload_to=attach_firefighting_check_upload_path,
        verbose_name='Файл акта проверки',
        )
    STATE_CHOICES = (
        ('Исправна', 'Исправна'),
        ('Неисправна', 'Неисправна'),
        ('Неустановлена', 'Неустановлена'),
        ('Не установлена', 'Не установлена'),
    )
    state = models.CharField(verbose_name='Состояние', max_length=20, choices=STATE_CHOICES)
    note = models.CharField(verbose_name='Примечание', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Проверка системы пожаротушения'
        verbose_name_plural = 'Проверки систем пожаротушения'
        ordering = ['-date']

    def __str__(self):
        return f'Проверка системы пожаротушения {self.firefighting_system.equipment.number}'


class FirefightingSystem(models.Model):
    """Установленные системы пожаротушения на оборудовании"""
    equipment = models.OneToOneField(
        to='equipments.Equipment',
        related_name='firefighting_system',
        verbose_name='Оборудование',
        on_delete=models.CASCADE,
        )
    requires_check = models.BooleanField(verbose_name='Требует проверки', default=True)

    class Meta:
        verbose_name = 'Система пожаротушения'
        verbose_name_plural = 'Системы пожаротушения'

    def __str__(self):
        return f'Система пожаротушения {self.equipment.number}'

    def get_last_check(self) -> FirefightingCheck | None:
        last_check = FirefightingCheck.objects.filter(firefighting_system=self).first()
        return last_check
