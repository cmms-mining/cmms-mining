# Generated by Django 5.1.1 on 2025-01-29 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0038_equipmetrunningtime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmetrunningtime',
            options={'ordering': ['-date'], 'verbose_name': 'Наработка оборудования', 'verbose_name_plural': 'Наработки оборудования'},
        ),
    ]
