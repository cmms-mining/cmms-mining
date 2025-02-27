# Generated by Django 4.1.7 on 2023-05-09 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("maintenance", "0001_initial"),
        ("equip_documents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EquipmentType",
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
                ("name", models.CharField(max_length=50, verbose_name="Название")),
                (
                    "icon",
                    models.ImageField(
                        blank=True, upload_to="icons", verbose_name="Иконка"
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
            ],
            options={
                "verbose_name": "Тип оборудования",
                "verbose_name_plural": "Типы оборудования",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="EquipmentModel",
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
                (
                    "manufacturer",
                    models.CharField(
                        blank=True, max_length=60, verbose_name="Производитель"
                    ),
                ),
                (
                    "equipment_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equipment_models",
                        to="equipments.equipmenttype",
                        verbose_name="Тип оборудования",
                    ),
                ),
            ],
            options={
                "verbose_name": "Модель оборудования",
                "verbose_name_plural": "Модели оборудования",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Equipment",
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
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "side_number",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Бортовой номер"
                    ),
                ),
                (
                    "serial_number",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="Серийный номер",
                    ),
                ),
                (
                    "note",
                    models.TextField(blank=True, null=True, verbose_name="Примечание"),
                ),
                (
                    "equipment_attachment_group",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equipments",
                        to="equip_documents.equipmentattachmentgroup",
                        verbose_name="Группа вложений",
                    ),
                ),
                (
                    "equipment_maintenance_group",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equipments",
                        to="maintenance.equipmentmaintenancegroup",
                        verbose_name="Группа обслуживания",
                    ),
                ),
                (
                    "equipment_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equipments",
                        to="equipments.equipmentmodel",
                        verbose_name="Модель оборудования",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оборудование",
                "verbose_name_plural": "Оборудование",
                "ordering": ["side_number"],
            },
        ),
    ]
