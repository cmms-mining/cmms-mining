# Generated by Django 5.1.1 on 2024-10-13 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0087_alter_buckettechstate_techstate_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalBucketRelocationAttachment',
        ),
    ]
