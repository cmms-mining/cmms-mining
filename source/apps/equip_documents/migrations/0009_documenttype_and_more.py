# Generated by Django 4.1.7 on 2023-05-13 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("equipments", "0002_remove_equipment_equipment_attachment_group"),
        ("equip_documents", "0008_equipmentattachmentgroup_slug_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentType",
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
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
            ],
            options={
                "verbose_name": "Тип документа",
                "verbose_name_plural": "Типы документов",
            },
        ),
        migrations.RemoveField(
            model_name="equipmentattachmentgroup",
            name="equipments",
        ),
        migrations.RemoveField(
            model_name="equipmentdocument",
            name="attachment_type",
        ),
        migrations.RemoveField(
            model_name="equipmentdocument",
            name="equipment",
        ),
        migrations.RemoveField(
            model_name="equipmentdocument",
            name="equipment_group",
        ),
        migrations.RemoveField(
            model_name="equipmentdocument",
            name="note",
        ),
        migrations.AddField(
            model_name="equipmentdocument",
            name="description",
            field=models.CharField(default=1, max_length=150, verbose_name="Описание"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="equipmentdocument",
            name="equipments",
            field=models.ManyToManyField(
                blank=True,
                related_name="equipment_documents",
                to="equipments.equipment",
                verbose_name="Оборудование",
            ),
        ),
        migrations.DeleteModel(
            name="AttachmentType",
        ),
        migrations.DeleteModel(
            name="EquipmentAttachmentGroup",
        ),
        migrations.AddField(
            model_name="equipmentdocument",
            name="document_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="equipment_documents",
                to="equip_documents.documenttype",
                verbose_name="Тип документа",
            ),
            preserve_default=False,
        ),
    ]