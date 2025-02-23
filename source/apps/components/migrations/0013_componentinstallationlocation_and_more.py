# Generated by Django 5.1.1 on 2024-10-03 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0012_alter_componenttype_options_component_component_type'),
        ('equipments', '0009_alter_nameplate_attachment_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentInstallationLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
            ],
        ),
        migrations.RemoveField(
            model_name='componenttype',
            name='equipment_models',
        ),
        migrations.CreateModel(
            name='ComponentTypeEquipmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.componenttype', verbose_name='Тип компонента')),
                ('equipment_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.equipmentmodel', verbose_name='Модель оборудования')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.componentinstallationlocation', verbose_name='Место установки')),
            ],
        ),
    ]
