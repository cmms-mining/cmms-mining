# Generated by Django 5.1.1 on 2024-10-03 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0075_alter_bucketdeinstallation_reason'),
        ('components', '0016_componentinstallation_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketinstallation',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_installations', to='components.componentinstallationlocation', verbose_name='Место установки'),
        ),
    ]
