# Generated by Django 5.1.5 on 2025-03-07 08:40

import apps.components.models.component
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0069_remove_component_requires_reconciliation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentattachment',
            name='attachment_file',
            field=models.FileField(upload_to=apps.components.models.component.component_attachment_upload_path, verbose_name='Файл'),
        ),
    ]
