# Generated by Django 5.1.1 on 2024-11-04 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_task_realizer_job_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['created_at'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
    ]