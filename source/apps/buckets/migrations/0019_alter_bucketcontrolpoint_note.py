# Generated by Django 4.1.7 on 2024-09-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0018_bucketcontrolpoint_bucketinspection_inspectionresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketcontrolpoint',
            name='note',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Примечание'),
        ),
    ]