# Generated by Django 5.1.1 on 2025-02-01 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userjobtitle_job_title'),
        ('tasks', '0029_remove_task_executor_job_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userjobtitle',
            name='job_title',
        ),
        migrations.RemoveField(
            model_name='userjobtitle',
            name='user',
        ),
        migrations.DeleteModel(
            name='JobTitle',
        ),
        migrations.DeleteModel(
            name='UserJobTitle',
        ),
    ]
