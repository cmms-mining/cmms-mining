# Generated by Django 5.1.1 on 2024-10-27 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_jobtitle_userjobtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userjobtitle',
            name='job_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_job_titles', to='accounts.jobtitle', verbose_name='Должность'),
        ),
    ]