# Generated by Django 5.1.1 on 2025-01-08 18:16

import apps.components.models.repair
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0062_componentrepairattachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='componentrepair',
            name='completed',
        ),
        migrations.AlterField(
            model_name='componentrepairattachment',
            name='attachment_file',
            field=models.FileField(upload_to=apps.components.models.repair.component_repair_attachment_upload_path, verbose_name='Файл'),
        ),
    ]
