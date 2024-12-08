import os

from django.db import models


class DocumentType(models.Model):
    """Типы документов (каталоги, инструкции и т.д."""
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'
        ordering = ['name']

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    upload_path = os.path.join(instance.document_type.slug, filename)
    return upload_path


class EquipmentDocument(models.Model):
    """Файлы документов оборудования (каталоги, инструкции, шильдики)"""
    attachment_file = models.FileField(upload_to=get_upload_path, verbose_name='Файл вложения')
    document_type = models.ForeignKey(
        to='equip_documents.DocumentType',
        related_name='equipment_documents',
        on_delete=models.CASCADE,
        verbose_name='Тип документа',
    )
    description = models.CharField(verbose_name='Описание', max_length=150)
    equipments = models.ManyToManyField(
        to='equipments.Equipment',
        related_name='equipment_documents',
        verbose_name='Оборудование',
        blank=True,
    )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, null=True, blank=True)
    created_at = models.DateField(verbose_name='Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Документ оборудования'
        verbose_name_plural = 'Документы оборудования'

    def __str__(self):
        return self.description
