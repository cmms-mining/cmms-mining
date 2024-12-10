# Generated by Django 5.1.1 on 2024-09-17 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0039_alter_bucketinspection_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bucketrelocation',
            old_name='reason',
            new_name='note',
        ),
        migrations.RemoveField(
            model_name='historicalbucketrelocation',
            name='reason',
        ),
        migrations.AddField(
            model_name='historicalbucketrelocation',
            name='note',
            field=models.TextField(default='1', verbose_name='Причина'),
            preserve_default=False,
        ),
    ]