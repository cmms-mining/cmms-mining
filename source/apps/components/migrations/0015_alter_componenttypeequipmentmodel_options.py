# Generated by Django 5.1.1 on 2024-10-03 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0014_alter_componentinstallationlocation_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='componenttypeequipmentmodel',
            options={'verbose_name': 'Место установки компонента на модели оборудования', 'verbose_name_plural': 'Мест установки компонентов на модели оборудования'},
        ),
    ]