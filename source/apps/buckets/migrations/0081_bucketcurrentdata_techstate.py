# Generated by Django 5.1.1 on 2024-10-10 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0080_alter_bucketrelocation_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketcurrentdata',
            name='techstate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buckets', to='buckets.buckettechstate', verbose_name='Местоположение'),
        ),
    ]
