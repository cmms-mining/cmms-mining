# Generated by Django 4.1.7 on 2024-08-26 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0004_bucketreceiving'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='number',
            field=models.CharField(max_length=3, null=True, verbose_name='Номер'),
        ),
    ]