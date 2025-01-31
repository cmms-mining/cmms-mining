from django.db import models


def component_attachment_upload_path(instance, filename):
    return f'documents/{instance.description}/{filename}'


class Document(models.Model):
    """Хранение докментов (распоряжений, приказов, шаблонов актов)"""

    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=component_attachment_upload_path,
    )
    description = models.CharField(verbose_name='Описание', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.description
