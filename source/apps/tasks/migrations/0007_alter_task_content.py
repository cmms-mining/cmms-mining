# Generated by Django 5.1.1 on 2024-10-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_done_task_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Содержимое'),
        ),
    ]