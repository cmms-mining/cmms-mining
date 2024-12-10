# Generated by Django 5.1.1 on 2024-10-03 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0013_componentinstallationlocation_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='componentinstallationlocation',
            options={'ordering': ['name'], 'verbose_name': 'Место установки компонента', 'verbose_name_plural': '(Справочник) Места установки компонентов'},
        ),
        migrations.AlterModelOptions(
            name='componenttypeequipmentmodel',
            options={'verbose_name': 'Место установки комонента на модели оборудования', 'verbose_name_plural': 'Мест установки комонентов на модели оборудования'},
        ),
        migrations.AlterField(
            model_name='componenttypeequipmentmodel',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='components.componentinstallationlocation', verbose_name='Место установки'),
        ),
    ]