# Generated by Django 5.1.1 on 2024-10-17 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0093_bucket_requires_reconciliation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='requires_reconciliation',
            field=models.BooleanField(default=True, verbose_name='Требует сверки'),
        ),
    ]