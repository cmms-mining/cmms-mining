# Generated by Django 4.1.7 on 2024-08-31 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0013_remove_bucketrelocation_note_bucketrelocation_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bucketrelocation',
            old_name='relocate_status',
            new_name='status',
        ),
    ]