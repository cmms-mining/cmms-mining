from django.contrib.auth.models import User
from django.db import models


class EventType(models.Model):
    """Типы событий"""
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тип событий'
        verbose_name_plural = 'Типы событий'

    def __str__(self):
        return self.name


class Event(models.Model):
    """События"""
    name = models.CharField(verbose_name='Название', max_length=100)
    event_type = models.ForeignKey(
        to='events.EventType',
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Тип события',
        )
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    time = models.TimeField(verbose_name='Время', blank=True, null=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Автор',
        )
    equipment = models.ForeignKey(
        to='equipments.Equipment',
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Оборудование',
        blank=True,
        )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.name} - {self.date}'


def get_eventfile_upload_path(instance, filename):
    # Генерируем путь сохранения файла, используя дату события
    return f'events/{instance.event.equipment.number}/{instance.event.date}/{instance.event.pk}/{filename}'


class EventFile(models.Model):
    """Файлы событий (в основном фотографии)"""
    attachment_file = models.FileField(upload_to=get_eventfile_upload_path, verbose_name='Файл')
    event = models.ForeignKey(
        to='events.Event',
        related_name='eventfiles',
        on_delete=models.CASCADE,
        verbose_name='Событие',
    )
    description = models.CharField(verbose_name='Описание', max_length=500, null=True, blank=True)
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, null=True, blank=True)
    created_at = models.DateField(verbose_name='Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Файл события'
        verbose_name_plural = 'Файлы событий'

    def __str__(self):
        return f'Файл события {self.event.name}'
