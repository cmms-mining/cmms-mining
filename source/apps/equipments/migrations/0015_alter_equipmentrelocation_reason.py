# Generated by Django 5.1.1 on 2024-10-15 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_techstateoption'),
        ('equipments', '0014_equipmentcurrentdata_relocation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentrelocation',
            name='reason',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.relocationreason', verbose_name='Причина'),
        ),
    ]
