# Generated by Django 5.1.1 on 2024-10-21 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0041_alter_component_serial_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='componenttask',
            options={'verbose_name': 'Задача компонента', 'verbose_name_plural': 'Задачи компонентов'},
        ),
    ]
