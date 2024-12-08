# Generated by Django 5.1.1 on 2024-10-09 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0076_bucketinstallation_location'),
        ('equipments', '0009_alter_nameplate_attachment_file_and_more'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketCurrentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bucket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_data', to='buckets.bucket', verbose_name='Ковш')),
                ('equipment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bucket', to='equipments.equipment', verbose_name='Местоположение')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buckets', to='sites.site', verbose_name='Местоположение')),
            ],
        ),
    ]
