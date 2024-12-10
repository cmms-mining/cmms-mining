# Generated by Django 5.1.1 on 2024-10-27 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userjobtitle_job_title'),
        ('tasks', '0014_task_accepted_for_execution'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='realizer_job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks_assigned', to='accounts.jobtitle', verbose_name='Исполнитель (должность)'),
        ),
    ]