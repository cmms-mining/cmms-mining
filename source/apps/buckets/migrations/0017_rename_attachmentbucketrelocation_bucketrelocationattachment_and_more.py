# Generated by Django 4.1.7 on 2024-09-02 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0016_attachmentbucketrelocation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AttachmentBucketRelocation',
            new_name='BucketRelocationAttachment',
        ),
        migrations.AlterModelOptions(
            name='bucketrelocationattachment',
            options={'verbose_name': 'Вложение перемещения ковша', 'verbose_name_plural': 'Вложения перемещения ковшей'},
        ),
    ]