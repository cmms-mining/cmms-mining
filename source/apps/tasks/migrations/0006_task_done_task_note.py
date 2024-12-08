# Generated by Django 5.1.1 on 2024-10-20 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
