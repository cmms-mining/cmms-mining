# Generated by Django 5.1.1 on 2024-09-28 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0050_alter_bucketrepair_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucketrelocation',
            name='received',
        ),
        migrations.RemoveField(
            model_name='historicalbucketrelocation',
            name='received',
        ),
    ]
