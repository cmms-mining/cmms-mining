# Generated by Django 4.1.7 on 2024-08-27 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0008_bucketrelocation_relocate_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketrelocation',
            name='send_date',
            field=models.DateField(default='2020-01-01', verbose_name='Дата отправки'),
            preserve_default=False,
        ),
    ]
