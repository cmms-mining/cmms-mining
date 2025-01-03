# Generated by Django 4.1.7 on 2023-10-31 12:18

import apps.events.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_equipments_eventfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventfile',
            name='attachment_file',
            field=models.FileField(upload_to=apps.events.models.get_eventfile_upload_path, verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='eventfile',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='eventfile',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventfiles', to='events.event', verbose_name='Событие'),
        ),
    ]
