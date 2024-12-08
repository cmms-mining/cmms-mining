# Generated by Django 5.1.1 on 2024-11-05 18:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_taskcomment_task'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='realizer',
            new_name='executor',
        ),
        migrations.AlterField(
            model_name='taskcomment',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='authored_tasks_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
