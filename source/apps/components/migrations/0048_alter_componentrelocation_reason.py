# Generated by Django 5.1.1 on 2024-11-24 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_techstateoption'),
        ('components', '0047_component_nomenclature_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentrelocation',
            name='reason',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='common.relocationreason', verbose_name='Причина'),
            preserve_default=False,
        ),
    ]
