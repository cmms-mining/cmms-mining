# Generated by Django 5.1.1 on 2025-01-11 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0003_alter_nomenclature_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
    ]
