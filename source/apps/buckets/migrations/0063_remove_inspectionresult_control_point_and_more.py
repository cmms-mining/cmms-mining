# Generated by Django 5.1.1 on 2024-10-01 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0062_alter_bucketdeinstallation_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspectionresult',
            name='control_point',
        ),
        migrations.RemoveField(
            model_name='bucketinspection',
            name='bucket',
        ),
        migrations.RemoveField(
            model_name='inspectionresult',
            name='inspection',
        ),
        migrations.DeleteModel(
            name='BucketControlPoint',
        ),
        migrations.DeleteModel(
            name='BucketInspection',
        ),
        migrations.DeleteModel(
            name='InspectionResult',
        ),
    ]
