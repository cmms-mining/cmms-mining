# Generated by Django 5.1.1 on 2024-10-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0023_componentcurrentdata_component_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentcurrentdata',
            name='relocation_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата перемещения'),
        ),
        migrations.AddField(
            model_name='componentcurrentdata',
            name='techstate_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата техсостояния'),
        ),
    ]
