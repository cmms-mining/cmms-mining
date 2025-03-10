# Generated by Django 5.1.1 on 2024-10-03 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0074_alter_bucketdeinstallation_from_equipment_and_more'),
        ('common', '0002_deinstallationreason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketdeinstallation',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='common.deinstallationreason', verbose_name='Причина'),
        ),
    ]
