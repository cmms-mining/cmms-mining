# Generated by Django 5.1.1 on 2024-11-24 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_techstateoption'),
        ('equipments', '0025_alter_equipmentrelocation_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentrelocation',
            name='reason',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.relocationreason', verbose_name='Причина'),
        ),
    ]