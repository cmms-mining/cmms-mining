# Generated by Django 5.1.1 on 2024-12-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0056_componentrepair_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='nomenclature_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Код номенклатуры'),
        ),
    ]
