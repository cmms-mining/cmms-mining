# Generated by Django 5.1.1 on 2024-10-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0013_alter_equipment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentcurrentdata',
            name='relocation_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата перемещения'),
        ),
        migrations.AddField(
            model_name='equipmentcurrentdata',
            name='techstate_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата техсостояния'),
        ),
    ]
