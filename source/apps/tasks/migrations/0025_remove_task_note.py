# Generated by Django 5.1.1 on 2024-11-29 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0024_remove_task_accepted_for_execution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='note',
        ),
    ]
