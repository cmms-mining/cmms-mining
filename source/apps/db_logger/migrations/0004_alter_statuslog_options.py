# Generated by Django 5.1.1 on 2024-10-13 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db_logger', '0003_statuslog_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuslog',
            options={'ordering': ('-create_datetime',), 'verbose_name': 'Логирование', 'verbose_name_plural': 'Логирование'},
        ),
    ]