# Generated by Django 5.1.1 on 2024-11-05 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_alter_task_options_taskcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcomment',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks.task', verbose_name='Задача'),
            preserve_default=False,
        ),
    ]
