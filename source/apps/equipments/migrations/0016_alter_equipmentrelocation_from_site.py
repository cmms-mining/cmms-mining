# Generated by Django 5.1.1 on 2024-10-15 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0015_alter_equipmentrelocation_reason'),
        ('sites', '0003_rename_is_contarctor_site_is_contractor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentrelocation',
            name='from_site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss_from_site', to='sites.site', verbose_name='Откуда'),
        ),
    ]
