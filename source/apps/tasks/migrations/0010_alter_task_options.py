# Generated by Django 5.1.1 on 2024-10-21 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_task_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_at'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
    ]
