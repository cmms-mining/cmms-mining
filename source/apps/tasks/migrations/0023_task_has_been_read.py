# Generated by Django 5.1.1 on 2024-11-22 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='has_been_read',
            field=models.BooleanField(default=False, verbose_name='Прочитана исполнителем'),
        ),
    ]
