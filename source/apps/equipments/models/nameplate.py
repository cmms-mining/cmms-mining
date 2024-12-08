from django.db import models


def equipment_upload_path(instance, filename):
    # Генерируем путь сохранения файла, используя имя оборудования и имя файла
    return f'nameplates/{instance.equipment.equipment_model.equipment_type.slug}' \
                     f'/{instance.equipment.equipment_model.name}' \
                     f'/{instance.equipment.number}/{filename}'


class Nameplate(models.Model):
    """Файлы документов оборудования (каталоги, инструкции, шильдики)"""
    attachment_file = models.FileField(upload_to=equipment_upload_path, verbose_name='Шильдик')
    equipment = models.ForeignKey(
        to='equipments.Equipment',
        related_name='nameplates',
        on_delete=models.CASCADE,
        verbose_name='Оборудование',
    )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, null=True, blank=True)
    created_at = models.DateField(verbose_name='Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Шильдик оборудования'
        verbose_name_plural = 'Шильдики оборудования'

    def __str__(self):
        return f'Шильдик {self.equipment.number}'
