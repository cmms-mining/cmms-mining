# Generated by Django 5.1.1 on 2024-11-24 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0050_alter_componentrelocation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentrelocation',
            name='date',
            field=models.DateField(null=True, verbose_name='Дата перемещения'),
        ),
    ]
