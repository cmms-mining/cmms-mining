# Generated by Django 5.1.1 on 2024-10-15 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='is_contarctor',
            field=models.BooleanField(default=False, verbose_name='Является подрядчиком'),
        ),
    ]
