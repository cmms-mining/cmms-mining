# Generated by Django 4.1.7 on 2023-05-09 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AttachmentType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип вложение",
                "verbose_name_plural": "Типы вложений",
            },
        ),
        migrations.CreateModel(
            name="EquipmentAttachmentGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Группа оборудования вложений",
                "verbose_name_plural": "Группы оборудования вложений",
            },
        ),
        migrations.CreateModel(
            name="EquipmentDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attachment_file",
                    models.FileField(
                        upload_to="equip_documents", verbose_name="Файл вложения"
                    ),
                ),
                (
                    "note",
                    models.CharField(
                        blank=True, max_length=75, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "file_size",
                    models.CharField(
                        blank=True,
                        max_length=30,
                        null=True,
                        verbose_name="Размер файла",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "attachment_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equipment_documents",
                        to="equip_documents.attachmenttype",
                        verbose_name="Тип вложения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Документ оборудования",
                "verbose_name_plural": "Документы оборудования",
            },
        ),
    ]
