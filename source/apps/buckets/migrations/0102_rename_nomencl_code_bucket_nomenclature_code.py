# Generated by Django 5.1.1 on 2025-01-23 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0101_delete_historicalbucketrepair'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bucket',
            old_name='nomencl_code',
            new_name='nomenclature_code',
        ),
    ]
