# Generated by Django 5.1.1 on 2025-01-20 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0026_task_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='content',
        ),
    ]
